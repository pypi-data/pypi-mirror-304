from typing import Any, Optional

from pydantic import BaseModel
from telebot_components.menu.menu import Menu as ComponentsMenu
from telebot_components.menu.menu import MenuConfig as ComponentsMenuConfig
from telebot_components.menu.menu import MenuHandler
from telebot_components.menu.menu import MenuItem as ComponentsMenuItem
from telebot_components.menu.menu import (
    MenuMechanism,
    TerminatorContext,
    TerminatorResult,
)

from telebot_constructor.user_flow.blocks.base import UserFlowBlock
from telebot_constructor.user_flow.types import (
    SetupResult,
    UserFlowContext,
    UserFlowSetupContext,
)
from telebot_constructor.utils import without_nones
from telebot_constructor.utils.pydantic import LocalizableText

NOOP_TERMINATOR = "noop"


class MenuItem(BaseModel):
    label: LocalizableText

    # exactly one field must be non-None
    submenu: Optional["Menu"] = None
    next_block_id: Optional[str] = None  # for terminal items
    link_url: Optional[str] = None  # for link buttons (works only if mechanism is inline)

    def model_post_init(self, __context: Any) -> None:
        specified_options = [o for o in (self.submenu, self.next_block_id, self.link_url) if o is not None]
        if len(specified_options) > 1:
            raise ValueError("At most one of the options may be specified: submenu, next block, or link URL")

        self._menu_terminator: str | None = NOOP_TERMINATOR if len(specified_options) == 0 else self.next_block_id

    def to_components_menu_item(self) -> ComponentsMenuItem:
        return ComponentsMenuItem(
            label=self.label,
            submenu=None if self.submenu is None else self.submenu.to_components_menu(),
            terminator=self._menu_terminator,
            link_url=self.link_url,
            bound_category=None,
        )


class MenuConfig(BaseModel):
    mechanism: MenuMechanism
    back_label: Optional[LocalizableText]
    lock_after_termination: bool


class Menu(BaseModel):
    text: LocalizableText
    items: list[MenuItem]
    config: MenuConfig

    def to_components_menu(self) -> ComponentsMenu:
        config = ComponentsMenuConfig(
            back_label=self.config.back_label,
            lock_after_termination=self.config.lock_after_termination,
            # TODO: convert markdown and plain texts to HTML and set is_text_html to True
            is_text_html=False,
            mechanism=self.config.mechanism,
        )
        return ComponentsMenu(
            text=self.text,
            menu_items=[item.to_components_menu_item() for item in self.items],
            config=config,
        )


class MenuBlock(UserFlowBlock):
    """Multilevel menu block powered by Telegram inline buttons"""

    menu: Menu

    def possible_next_block_ids(self) -> list[str]:
        return without_nones([item.next_block_id for item in self.menu.items])

    def model_post_init(self, __context: Any) -> None:
        self.menu.to_components_menu()  # to validate

    @property
    def menu_handler(self) -> MenuHandler:
        if self._components_menu_handler is None:
            raise RuntimeError("self.menu_handler called before setup method")
        return self._components_menu_handler

    async def enter(self, context: UserFlowContext) -> None:
        await self.menu_handler.start_menu(bot=context.bot, user=context.user)

    async def setup(self, context: UserFlowSetupContext) -> SetupResult:
        self._components_menu = self.menu.to_components_menu()
        self._components_menu_handler = MenuHandler(
            name=self.block_id,
            bot_prefix=context.bot_prefix,
            menu_tree=self._components_menu,
            redis=context.redis,
            category_store=None,
            language_store=context.language_store,
        )

        async def on_terminal_menu_option_selected(terminator_context: TerminatorContext) -> Optional[TerminatorResult]:
            terminator = terminator_context.terminator
            if terminator != NOOP_TERMINATOR:
                next_block_id = terminator
                await context.enter_block(
                    next_block_id,
                    UserFlowContext.from_setup_context(
                        setup_ctx=context,
                        chat=(
                            terminator_context.menu_message.chat
                            if terminator_context.menu_message is not None
                            else None
                        ),
                        user=terminator_context.user,
                        last_update_content=terminator_context.menu_message,
                    ),
                )
            return None

        self.menu_handler.setup(
            bot=context.bot,
            on_terminal_menu_option_selected=on_terminal_menu_option_selected,
        )
        return SetupResult.empty()

"""Get additional items."""

import logging

from playwright.async_api import Page

from cookidoo_api.actions import selector, state_waiter
from cookidoo_api.const import (
    DEFAULT_RETRIES,
    SHOPPING_LIST_ADDITIONAL_CHECKED_ITEMS_SELECTOR,
    SHOPPING_LIST_ADDITIONAL_ITEM_ID_ATTR,
    SHOPPING_LIST_ADDITIONAL_ITEM_ID_SUB_SELECTOR,
    SHOPPING_LIST_ADDITIONAL_ITEM_LABEL_SUB_SELECTOR,
    SHOPPING_LIST_ADDITIONAL_ITEM_SUB_SELECTOR,
    SHOPPING_LIST_ADDITIONAL_ITEMS_SELECTOR,
)
from cookidoo_api.exceptions import CookidooException
from cookidoo_api.types import CookidooConfig, CookidooItem, CookidooItemStateType

_LOGGER = logging.getLogger(__name__)


async def get_additional_items(
    cfg: CookidooConfig,
    page: Page,
    out_dir: str,
    pending: bool = False,
    checked: bool = False,
) -> list[CookidooItem]:
    """Get additional items.

    Parameters
    ----------
    cfg
        Cookidoo config
    page
        The page, which should have been validated already
    out_dir
        The directory to store output such as trace or screenshots
    pending
        Get the pending items
    checked
        Get the checked items

    Returns
    -------
    list[CookidooItem]
        The list of the items

    Raises
    ------
    CookidooSelectorException
        When the page does not behave as expected and some content is not available

    """

    additional_items: list[CookidooItem] = []

    async def items_for(sel: str, state: CookidooItemStateType) -> None:
        _LOGGER.debug("Wait for additional items: %s", sel)
        await state_waiter(page, sel, "attached")

        # Select the parent element
        _LOGGER.debug("Extract parent list: %s", sel)
        parent = await selector(page, sel)
        if await parent.is_hidden():
            _LOGGER.debug(
                "Parent list is hidden, no additional items available for: %s", sel
            )
            return

        # Get the children of the parent element
        _LOGGER.debug(
            "Extract additional items from parent: %s / %s",
            sel,
            SHOPPING_LIST_ADDITIONAL_ITEM_SUB_SELECTOR,
        )
        children = await parent.query_selector_all(
            SHOPPING_LIST_ADDITIONAL_ITEM_SUB_SELECTOR
        )

        # Loop through the children and perform actions
        for i, child in enumerate(children):
            _logger = _LOGGER.getChild(f"{i}")
            _logger.debug("Extract elements")
            label_el, id_el = [
                await child.query_selector(item_sel)
                for item_sel in [
                    SHOPPING_LIST_ADDITIONAL_ITEM_LABEL_SUB_SELECTOR,
                    SHOPPING_LIST_ADDITIONAL_ITEM_ID_SUB_SELECTOR,
                ]
            ]

            if not id_el:
                _logger.warning(
                    "Skip as required data 'id' (%s) not found:\n%s",
                    SHOPPING_LIST_ADDITIONAL_ITEM_ID_SUB_SELECTOR,
                    await child.inner_html(),
                )
                continue
            if not label_el:
                _logger.warning(
                    "Skip as required data 'label' (%s) not found:\n%s",
                    SHOPPING_LIST_ADDITIONAL_ITEM_LABEL_SUB_SELECTOR,
                    await child.inner_html(),
                )
                continue

            _logger.debug("Extract information")
            id = await id_el.get_attribute(SHOPPING_LIST_ADDITIONAL_ITEM_ID_ATTR)
            label = await label_el.text_content()
            if not id:
                _logger.warning(
                    "Skip as id (%s) is empty:\n%s",
                    SHOPPING_LIST_ADDITIONAL_ITEM_ID_SUB_SELECTOR,
                    await id_el.inner_html(),
                )
                continue
            if not label:
                _logger.warning(
                    "Skip as label (%s) is empty:\n%s",
                    SHOPPING_LIST_ADDITIONAL_ITEM_LABEL_SUB_SELECTOR,
                    await label_el.inner_html(),
                )
                continue
            additional_item = CookidooItem(
                {
                    "label": label,
                    "description": None,
                    "id": id,
                    "state": state,
                }
            )
            _logger.debug("Data: %s", additional_item)
            additional_items.append(additional_item)

    for retry in range(cfg.get("retries", DEFAULT_RETRIES)):
        try:
            additional_items = []
            # empty_list_message_el = await page.query_selector(
            #     SHOPPING_LIST_EMPTY_SELECTOR
            # )
            # _LOGGER.debug(empty_list_message_el)
            # if empty_list_message_el and not await empty_list_message_el.is_hidden():
            #     break
            if pending:
                _LOGGER.debug("Get pending additional items")
                await items_for(SHOPPING_LIST_ADDITIONAL_ITEMS_SELECTOR, "pending")
            if checked:
                _LOGGER.debug("Get checked additional items")
                await items_for(
                    SHOPPING_LIST_ADDITIONAL_CHECKED_ITEMS_SELECTOR, "checked"
                )
        except CookidooException as e:
            if retry < cfg.get("retries", DEFAULT_RETRIES):
                _LOGGER.warning(
                    "Could not get additional items on try #%d due to error:\n%s",
                    retry,
                    e,
                )
            else:
                _LOGGER.warning(
                    "Exhausted all #%d retries for get additional items",
                    retry + 1,
                )
                raise CookidooException("Could not get additional items") from e
    return additional_items

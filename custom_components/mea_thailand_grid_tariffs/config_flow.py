"""Config flow ของ MEA Thailand Grid Tariffs."""
from __future__ import annotations

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_SUB_TARIFF,
    CONF_TARIFF,
    DOMAIN,
    TARIFF_PAGES,
    business_title,
    residential_title,
)

# sub_tariff options แยกตามประเภท tariff — value มีชื่อเป็น "type_2_..." (ดู SUB_TARIFF_ID_SLUGS)
TARIFF_SUB_OPTIONS: dict[str, list[str]] = {
    "residential": ["le150", "gt150", "tou_131", "tou_132"],
    "business": ["sb_211", "sb_212", "sb_tou_221", "sb_tou_222"],
}


class MeaTariffConfigFlow(ConfigFlow, domain=DOMAIN):
    """จัดการขั้นตอนเพิ่ม integration."""

    VERSION = 1

    def __init__(self) -> None:
        self._selected_tariff: str = "residential"

    async def async_step_user(self, user_input=None):
        """ขั้นตอนแรก: เลือกประเภท tariff (Residential / Business)."""
        if user_input is not None:
            self._selected_tariff = user_input[CONF_TARIFF]
            return await self.async_step_sub_tariff()

        schema = vol.Schema(
            {
                vol.Required(CONF_TARIFF, default="residential"): SelectSelector(
                    SelectSelectorConfig(
                        options=list(TARIFF_PAGES.keys()),
                        mode=SelectSelectorMode.LIST,
                        translation_key="tariff",
                    )
                ),
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_sub_tariff(self, user_input=None):
        """ขั้นตอนที่สอง: เลือก sub_tariff ตามประเภทที่เลือกไว้."""
        if user_input is not None:
            sub_key = user_input[CONF_SUB_TARIFF]
            tariff_key = self._selected_tariff
            unique_id = f"{tariff_key}_{sub_key}"

            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            title = (
                residential_title(self.hass.config.language)
                if tariff_key == "residential"
                else business_title(self.hass.config.language)
            )

            return self.async_create_entry(
                title=title,
                data={
                    CONF_TARIFF: tariff_key,
                    CONF_SUB_TARIFF: sub_key,
                },
            )

        options = TARIFF_SUB_OPTIONS[self._selected_tariff]
        # กำหนดเฉพาะ value ใน options แล้วให้ Home Assistant ดึง Label จาก selector.sub_tariff.options ตามภาษาของผู้ใช้
        schema = vol.Schema(
            {
                vol.Required(CONF_SUB_TARIFF, default=options[0]): SelectSelector(
                    SelectSelectorConfig(
                        options=options,
                        mode=SelectSelectorMode.LIST,
                        translation_key="sub_tariff",
                    )
                ),
            }
        )

        return self.async_show_form(step_id="sub_tariff", data_schema=schema)

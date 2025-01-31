from datetime import date

from aiogram.types import InlineKeyboardButton
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Calendar, CalendarScope, CalendarConfig
from aiogram_dialog.widgets.kbd.calendar_kbd import CalendarScopeView, CalendarDaysView, CalendarMonthView, \
    CallbackGenerator, BEARING_DATE, CALLBACK_SCOPE_MONTHS, CalendarData
from aiogram_dialog.widgets.text import Format

from src.custom_widgets.i18n_format import I18NFormat


class BirthdateAskingCalendarMonthView(CalendarMonthView):
    def __init__(self, callback_generator: CallbackGenerator):
        super().__init__(callback_generator, this_month_text=Format('{date:%B}'))

    async def _render_header(
            self, config, offset, data, manager,
    ) -> list[InlineKeyboardButton]:
        return []

    async def _render_pager(
            self,
            config: CalendarConfig,
            offset: date,
            data: dict,
            manager: DialogManager,
    ) -> list[InlineKeyboardButton]:
        return []


class BirthdateAskingCalendarDaysView(CalendarDaysView):
    def __init__(self, callback_generator: CallbackGenerator):
        super().__init__(callback_generator,
                         zoom_out_text=I18NFormat('back'),
                         header_text=Format("🗓 {date:%B}"),
                         today_text=Format('{date:%d}'))

    async def _render_week_header(
            self,
            config: CalendarConfig,
            data: dict,
            manager: DialogManager,
    ) -> list[InlineKeyboardButton]:
        return []

    async def _render_pager(
            self,
            config: CalendarConfig,
            offset: date,
            data: dict,
            manager: DialogManager,
    ) -> list[InlineKeyboardButton]:
        curr_month = offset.month

        curr_month_data = {
            "month": curr_month,
            "date": BEARING_DATE.replace(month=curr_month),
            "data": data,
        }
        zoom_button = InlineKeyboardButton(
            text=await self.zoom_out_text.render_text(
                curr_month_data, manager,
            ),
            callback_data=self.callback_generator(CALLBACK_SCOPE_MONTHS),
        )
        return [zoom_button]

class BirthdateAskingCalendar(Calendar):
    def _init_views(self) -> dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.MONTHS: BirthdateAskingCalendarMonthView(self._item_callback_data),
            CalendarScope.DAYS: BirthdateAskingCalendarDaysView(self._item_callback_data),
        }

    def get_scope(self, manager: DialogManager) -> CalendarScope:
        calendar_data: CalendarData = self.get_widget_data(manager, {})
        current_scope = calendar_data.get("current_scope")
        if not current_scope:
            return CalendarScope.MONTHS
        try:
            return CalendarScope(current_scope)
        except ValueError:
            # LOG
            return CalendarScope.MONTHS

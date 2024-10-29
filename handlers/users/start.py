from http.client import responses
from tkinter.ttk import Button

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.menu import menu_start
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import requests
from aiogram.types import CallbackQuery
import os
from keyboards.inline.weather_buttons import get_forecast_buttons


from loader import dp, bot
import requests


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text="Assalumo alekum ob-havo botiga xush kelibsiz"
    await message.answer(text,reply_markup=menu_start)


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def location_addres_function(message:types.Message):
    lon=message.location.longitude
    lat=message.location.latitude

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max&timezone=auto"
    response=requests.get(url)

    if response.status_code==200:
        data=response.json()
        if "daily" in data:
            today=data['daily']['time'][0]
            temp_max=data['daily']['temperature_2m_max'][0]
            temp_max=data['daily']['temperature_2m_min'][0]
            precipitation=data['daily']['precipitation_sum'][0]
            win_speed=data['daily']['windspeed_10m_max'][0]

            answer=(
                f"🗓**Sana:**{today}\n\n"
                f"🔼**Eng yuqori harorat:**{ temp_max}°C\n"
                f"🔽**Eng past harorat:**{ temp_max}°C\n"
                f"🌧**Yog'ingarchilik:**{ precipitation}°C\n"
                f"💨**Shamol tezligi:**{ win_speed}°C\n"
            )

        else:
            answer = (
                f"❌kunlik ob-havo ma'lumotlar mavjud emas."

            )
    else:
        answer = (
            f"❌xatolik yuz berdi : {response.status_code}"

        )

    await message.answer(answer,parse_mode="Markdown",reply_markup=get_forecast_buttons(lat,lon))



@dp.callback_query_handler(lambda c:c.data.startswith('forecast_'))
async  def Buttons_callback_text(callback_query:CallbackQuery):
    _,days,lat,lon=callback_query.data.split('_')
    days=int(days)


    url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max&timezone=auto")

    response=requests.get(url)
    if response.status_code==200:
        data =response.json()
        if 'daily' in data:
            answer=f"🗓**{days}:**kunlik ob-havo ma'lumotlari\n\n"
            for i in range(min(days,len(data['daily']['time']))):
                today = data['daily']['time'][i]
                temp_max = data['daily']['temperature_2m_max'][i]
                temp_max = data['daily']['temperature_2m_min'][i]
                precipitation = data['daily']['precipitation_sum'][i]
                win_speed = data['daily']['windspeed_10m_max'][i]

                answer += (
                    f"🗓**sana:**{today}\n\n"
                    f"🔼**Eng yuqori harorat:**{temp_max}°C\n"
                    f"🔽**Eng past harorat:**{temp_max}°C\n"
                    f"🌧**yog'ingarchilik:**{precipitation}°C\n"
                    f"💨**shamol tezligi:**{win_speed}°C\n"
                )
        else:
                answer = (
                    f"❌kunlik ob-havo ma'lumotlar mavjud emas."

                )
    else:
            answer = (
                f"❌xatolik yuz berdi : {response.status_code}"

            )
            await callback_query.message.answer(answer, parse_mode="Markdown", reply_markup=get_forecast_buttons(lat, lon))
            await callback_query.message.answer()


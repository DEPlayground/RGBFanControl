/*
    Lara Maia <dev@lara.click> 2019

    The RGBFanControl is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    The RGBFanControl is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see http://www.gnu.org/licenses/.
*/

struct front_fans_params
{
    static const unsigned int fan_count = 3;

    const byte fan_power_pin[fan_count] = {PORTD7, PORTD4, PORTD6};
    const byte fan_speed_pin[fan_count] = {PORTC0, PORTC2, PORTC1};
    const byte led_power_pin[fan_count] = {PORTB4, PORTD3, PORTD5};
    const byte rgb_pin[fan_count] = {PORTB2, PORTB3, PORTB1};

    const char fan_power_register[fan_count] = {'D', 'D', 'D'};
    const char fan_speed_register[fan_count] = {'C', 'C', 'C'};
    const char led_power_register[fan_count] = {'B', 'D', 'D'};
    const char rgb_register[fan_count] = {'B', 'B', 'B'};

    unsigned int fan_speed[fan_count] = {600, 600, 600};
    unsigned int fan_speed_frequency[fan_count] = {0, 0, 0};
    unsigned int hue[fan_count] = {0, 0, 0};
};
struct front_fans_params front_params;

struct front_fans_settings
{
    byte fan_power[front_params.fan_count] = {1, 1, 1};
    byte led_power[front_params.fan_count] = {0, 0, 0};
    byte rgb[front_params.fan_count][3] = {{255, 0, 0}, {255, 0, 0}, {255, 0, 0}};
    byte pulse_sync = 1;
    
    unsigned int effect_id[front_params.fan_count] = {0, 0, 0};
    unsigned int p_delay[front_params.fan_count] = {6, 6, 6};
    unsigned int p_divisor[front_params.fan_count] = {4, 4, 4};
    unsigned int p_multiplier[front_params.fan_count] = {2, 2, 2};
};
struct front_fans_settings front_settings;

struct back_fans_params
{
    static const unsigned int fan_count = 1;
    static const unsigned int led_count = 29;
    static const byte data_pin = 8;

    CRGB leds[led_count];

    unsigned int hue[led_count];
};
struct back_fans_params back_params;

struct back_fans_settings
{
    byte rgb[back_params.led_count][3];
    byte pulse_sync = 1;

    unsigned int effect_id[back_params.fan_count];
    unsigned int p_delay = 1;
    unsigned int p_divisor = 1;
    unsigned int p_multiplier = 1;
};
struct back_fans_settings back_settings;
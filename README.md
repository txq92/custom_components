# Homeassistant
# custom_components lịch âm
Tải thư mục lịch âm và chép vào thư mục custom_components trong hass


Thêm trong configuration:

```sh
sensor:
  - platform: lich_am

```

Thêm trong automation
```sh
automation:
  # Auto Nhắc rằm và mùng 1 qua ViPi vào 6h sáng và 18h tối vào trước 1 ngày và ngày rằm + mùng 1
  - id: '0001'
    alias: Nhắc rằm mùng 1
    trigger:
      - platform: time
        at: '06:00:00'
      - platform: time
        at: '18:00.:00'
    action:
      - service: script.phat_loa_vipi
        data_template:
          message: >           
            {% set ngay_mai = states('sensor.am_lich_ngay_mai') %}
            {% set ngay_mai_int = ngay_mai.split('/')[0] | int %}
            {% set ngay_hom_nay = states('sensor.am_lich_hom_nay') %}
            {% set ngay_hom_nay_int = ngay_hom_nay.split('/')[0] | int %}
            {% if ngay_mai_int == 1 %}
              "Bản tin thông báo: Ngày mai là mùng 1 âm lịch. Nhằm {{ states('sensor.ngay_am_ngay_mai') }}."
              "giờ tốt {{ states('sensor.gio_tot_ngay_mai') }} giờ xấu là giờ: {{ states('sensor.gio_xau_ngay_mai') }}."
            {% elif ngay_mai_int == 15 %}
              "Bản tin thông báo: Ngày mai là rằm. Nhằm {{ states('sensor.ngay_am_ngay_mai') }}."
              " ngày mai {{ states('sensor.gio_tot_ngay_mai') }} giờ xấu là giờ:{{ states('sensor.gio_xau_ngay_mai') }}."
            {% elif ngay_hom_nay_int == 15 %}
              "Bản tin thông báo: Hôm nay là rằm. Nhằm  {{ states('sensor.ngay_am_hom_nay') }}."
              "giờ tốt là giờ: {{ states('sensor.gio_tot_hom_nay') }} giờ xấu là giờ: {{ states('sensor.gio_xau_hom_nay') }}."
            {% elif ngay_hom_nay_int == 1 %}
              "Bản tin thông báo: Hôm nay là mùng 1. Nhằm {{ states('sensor.ngay_am_hom_nay') }}."
              "giờ tốt là giờ: {{ states('sensor.gio_tot_hom_nay') }} giờ xấu là giờ: {{ states('sensor.gio_xau_hom_nay') }}."
            {% endif %}  

   ```
# custom_components edge_tts
Tải thư mục edge_tts và chép vào thư mục custom_components trong hass


Thêm trong configuration:
```sh
tts:
  - platform: edge_tts
    service_name: edge
    language: vi-VN-HoaiMyNeural
    volume: +10%
    rate: -10%

   ```
Ví dụ về scrip phát giọng Nữ edge-tts qua loa google
```sh
  phat_loa_phong_khach:
    alias: "script phat loa phòng khách"
    sequence:
      - service: media_player.volume_set
        target:
          entity_id: media_player.phong_khach_2
        data_template:
          volume_level: "{{ volume | default(0.5) }}"  # Sử dụng giá trị mặc định là 0.5 nếu không có giá trị được cung cấp
      - service: tts.edge
        data_template:
          entity_id: media_player.phong_khach_2
          message: "{{ message }}"

  test_script_media_pk:
    alias: Test script phát media player phòng khách
    sequence:
      - service: script.phat_loa_phong_khach
        data:
          message: 'đây là scrip test loa media player phòng khách'
          volume: 0.5  # Thay 0.5 bằng mức âm lượng mong muốn (giữa 0 và 1)
   ```

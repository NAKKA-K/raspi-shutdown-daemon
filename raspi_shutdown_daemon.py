#!/usr/bin/env python3
import os
import sys
import RPi.GPIO as GPIO
import time
import pygame.mixer
import argparse
import tempfile

# 5秒間スイッチを長押しすると、シャットダウンする
# 長押ししている間はLEDが光る
# defalt: LED1(PIN21) & SW1(PIN7)
def raspi_shutdown_unit(SW1=7, LED1=21):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SW1, GPIO.IN)
    GPIO.setup(LED1, GPIO.OUT)

    cnt = 0
    while 1:
        if GPIO.input(SW1) == 1:
            cnt += 1
        else:
            cnt = 0

        if cnt >= 25:
            info_shutdown_daemon('!!!!! This raspi shutdown !!!!!')
            os.system('sudo shutdown -h now')

        GPIO.output(LED1, cnt)
        time.sleep(0.2)


# このデーモン用log
def info_shutdown_daemon(info):
    print(info)

    args = get_flags()
    if args.alert:
        alert_message_at_shutdown("シャットダウンします")

# CL引数のパース
def get_flags():
    parser = argparse.ArgumentParser()
    parser.add_argument("--alert", help="Alert message at shutdown.", action="store_true")
    return parser.parse_args()

def alert_message_at_shutdown(message):
    temp_wav = '/tmp/temp_damemon.wav'
    try:
        make_alert_wav(temp_wav, message)
        pygame.mixer.init()
        pygame.mixer.music.load(temp_wav)
        pygame.mixer.music.play()
    finally:
        os.remove(temp_wav)

def make_alert_wav(file_name, message):
    jtalk_option="\
        -m /usr/share/hts-voice/mei/mei_normal.htsvoice \
        -x /var/lib/mecab/dic/open-jtalk/naist-jdic \
        -ow {}".format(file_name)
    os.system("echo {} | open_jtalk {}".format(message, jtalk_option))

# プロセスのフォークと親プロセスの終了
def fork():
    pid = os.fork()
    if pid:
        write_pid(pid)
        sys.exit()

# pidファイルへ書き込み
def write_pid(pid):
    with open('/var/run/raspi_shutdown_daemon.pid', 'w') as pid_file:
        pid_file.write(str(pid)+"\n")

# deamonプロセスの起動
def daemon():
    fork() # 親プロセスを殺し、子プロセスを孤児化させる
    os.setsid()
    fork() # セッションリーダーを殺し、プロセスを完全に独立化

    raspi_shutdown_unit()

if __name__ == '__main__':
    daemon()

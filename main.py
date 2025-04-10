def on_button_pressed_a():
    radio.send_value("status", 1)
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    radio.send_value("status", 2)
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_received_value(name, value):
    global people, diameter
    if name == "commande":
        if value == 1:
            Démarer()
        if True:
            Arreter()
    if name == "people":
        people = value
    if name == "diameter":
        diameter = 0
radio.on_received_value(on_received_value)

def Démarer():
    global tour
    for index in range(people):
        radio.send_value("find", 0)
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR,
            maqueenPlusV2.MyEnumDir.FORWARD,
            255)
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR,
            maqueenPlusV2.MyEnumDir.FORWARD,
            50)
        if huskylens.is_appear(1, HUSKYLENSResultType_t.HUSKYLENS_RESULT_BLOCK):
            maqueenPlusV2.control_motor_stop(maqueenPlusV2.MyEnumMotor.ALL_MOTOR)
            radio.send_value("find", 1)
            music.play(music.builtin_playable_sound_effect(soundExpression.giggle),
                music.PlaybackMode.UNTIL_DONE)
            basic.show_string("Comment vas tu ? ")
            basic.show_string("A : ")
            basic.show_icon(IconNames.HAPPY)
            basic.show_string("B : ")
            basic.show_icon(IconNames.SAD)
        tour += 1
def Arreter():
    maqueenPlusV2.control_motor_stop(maqueenPlusV2.MyEnumMotor.ALL_MOTOR)
tour = 0
people = 0
diameter = 0
music._play_default_background(music.built_in_playable_melody(Melodies.POWER_UP),
    music.PlaybackMode.IN_BACKGROUND)
diameter = 120
people = 5
maqueenPlusV2.i2c_init()
huskylens.init_i2c()
huskylens.init_mode(protocolAlgorithm.ALGORITHM_FACE_RECOGNITION)
radio.set_group(67)

def on_forever():
    huskylens.request()
    basic.pause(100)
    if maqueenPlusV2.read_ultrasonic(DigitalPin.P13, DigitalPin.P14) <= 5:
        basic.show_icon(IconNames.BUTTERFLY)
        radio.send_string("Obstacle")
        maqueenPlusV2.control_motor_stop(maqueenPlusV2.MyEnumMotor.ALL_MOTOR)
    else:
        basic.show_icon(IconNames.YES)
    radio.send_value("accelerationy", input.acceleration(Dimension.Y))
    radio.send_value("accelerationx", input.acceleration(Dimension.X))
    radio.send_value("temperature", input.temperature())
    radio.send_value("niveausonore", input.sound_level())
    radio.send_value("signal",
        radio.received_packet(RadioPacketProperty.SIGNAL_STRENGTH))
basic.forever(on_forever)

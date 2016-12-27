def releTest():
    while(True):
        wiringpi.digitalWrite(FUN_RELE, wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(FOG_RELE, wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(PUMP_RELE, wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(UNCONNECTED, wiringpi.GPIO.LOW)
        sleep(5)

        wiringpi.digitalWrite(FUN_RELE, wiringpi.GPIO.HIGH)
        wiringpi.digitalWrite(FOG_RELE, wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(PUMP_RELE, wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(UNCONNECTED, wiringpi.GPIO.LOW)
        sleep(5)

        wiringpi.digitalWrite(FUN_RELE, wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(FOG_RELE, wiringpi.GPIO.HIGH)
        wiringpi.digitalWrite(PUMP_RELE, wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(UNCONNECTED, wiringpi.GPIO.LOW)
        sleep(5)

        wiringpi.digitalWrite(FUN_RELE, wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(FOG_RELE, wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(PUMP_RELE, wiringpi.GPIO.HIGH)
        wiringpi.digitalWrite(UNCONNECTED, wiringpi.GPIO.LOW)
        sleep(5)

        wiringpi.digitalWrite(FUN_RELE, wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(FOG_RELE, wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(PUMP_RELE, wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(UNCONNECTED, wiringpi.GPIO.HIGH)
        sleep(5)


from dronekit import connect, VehicleMode
import time

def takeoff():
    log = []
    try:
        vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True, timeout=60, heartbeat_timeout=60)
        log.append("Connected to vehicle.")

        while not vehicle.is_armable:
            log.append("Waiting for vehicle to become armable...")
            time.sleep(1)

        vehicle.mode = VehicleMode("GUIDED")
        log.append("Mode set to GUIDED")
        time.sleep(1)

        vehicle.armed = True
        log.append("Arming drone...")

        arm_timeout = 30
        start = time.time()
        while not vehicle.armed and (time.time() - start) < arm_timeout:
            log.append("Waiting for arming...")
            time.sleep(1)

        if not vehicle.armed:
            log.append("Arming timed out!")
            vehicle.close()
            return log

        vehicle.simple_takeoff(10)  # 10 meters
        log.append("Takeoff initiated...")

        while True:
            alt = vehicle.location.global_relative_frame.alt
            log.append(f"Altitude: {alt:.2f} m")
            if alt >= 9.5:
                break
            time.sleep(1)

        log.append("Reached target altitude. Landing...")
        vehicle.mode = VehicleMode("LAND")
        time.sleep(5)

        vehicle.close()
        log.append("Landed and closed connection.")
        return log

    except Exception as e:
        log.append(f"Error: {str(e)}")
        return log

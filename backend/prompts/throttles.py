from rest_framework.throttling import UserRateThrottle

class BurstRateThrottle(UserRateThrottle):
    rate = "1/second"

class SustainedRateThrottle(UserRateThrottle):
    rate = "10/minute"

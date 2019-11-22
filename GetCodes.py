"""Simple example showing how to get gamepad events."""

from __future__ import print_function


from inputs import get_gamepad
codes = ["SYN_REPORT",0]

def main():
    """Just print out some event infomation when the gamepad is used."""
    while 1:

        events = get_gamepad()
        for event in events:

            #print(event.ev_type, event.code, event.state)
            if (event.code not in codes):
                print("Codes:")
                codes.append(event.code)
                print(codes)
                #codes = codes
if __name__ == "__main__":
    main()

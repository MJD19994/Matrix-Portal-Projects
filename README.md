This is a place for me to share my ongoing work, I found a few projects for the Matrix Portals but none that really fit what I needed or wanted so I set out on my own.
I will share all my projects here, just note they are all a work in progress. My goal is to create very customizable code so someone else can edit it to fit their own set up (IE. Screen Size, Color Mappings, ETC). 


I have found that some matrix panels represent colors different so here are some troubleshooting steps

1) Verify Wiring and Pin Configuration:
    Many color discrepancies (such as red and blue being reversed) are caused by minor differences in how the display is wired. Verify that each color pin (red, green, blue) is correctly connected. If a you find that the colors        are swapped, you can adjust the order in the rgb_pins array. For example, if red and blue are reversed, you might swap your board.MTX_R1 with board.MTX_B1 (and similarly for your second set) in the code

2) Use this simple test routine that displays solid color blocks/stripes (Each for Red, Green, Blue, White). This way you can visually check if each channel is performing as expected:


    	def display_color_test():
    	    test_group = displayio.Group()
    	    # Create solid rectangles for red, green, blue, and white.
    	    red_rect = Rect(0, 0, 16, 64, fill=0xFF0000)
    	    green_rect = Rect(16, 0, 16, 64, fill=0x00FF00)
    	    blue_rect = Rect(32, 0, 16, 64, fill=0x0000FF)
    	    white_rect = Rect(48, 0, 16, 64, fill=0xFFFFFF)
    	    test_group.append(red_rect)
    	    test_group.append(green_rect)
    	    test_group.append(blue_rect)
    	    test_group.append(white_rect)
    	    display.root_group = test_group
    	
    	# Call this function to run the test.
    	display_color_test()
  

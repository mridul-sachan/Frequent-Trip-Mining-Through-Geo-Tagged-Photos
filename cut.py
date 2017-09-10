        # arcsin_arg is calculating the argument value of arcsin() as given in equation 4 under Photo Collection Segmentation.

        arcsin_arg = math.sqrt(
            math.sin(del_delta / 2) ** 2 + (math.cos(lat2) * math.cos(lat1) * math.sin(del_lambda / 2) ** 2))

        ''' Function math.asin(x) Returns the arc sine of x, in radians.
                    Refer https://docs.python.org/2/library/math.html for more details.'''

        phi_rad = 2 * math.asin(arcsin_arg)  # Equation 4 -- page 136
        # 6370Km is D i.e. radius of the Earth.

        if phi_rad == 0 : # if phi_rad will be zero then log function will throw an error so changing to non-zero value.
            phi_rad = 0.1

        # Calculating the value of distance gaps :
        distance_gap = math.log10(6370 * phi_rad)  # Equation 3 second part
        #print distance_gap



'''image_info_db[len(image_info_db) - 1] = ??

// gn
// if gn >
//      push current set into list
//      put currennt element into new set

'''
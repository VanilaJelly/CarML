OBD Data analysis
===================

Calculating Fuel Efficiency
---------------------------

1.  Problem : Given dataset does not contain distance traveled
=> Calculate distance using speed, time

    dist[i] = (time[i+1] - time[i]) * (speed[i+1]-speed[i]/2)

If time[i+1] - time[i] > 120 (2 min), fix it to 2min

2. Problem : Noise in Fuel Level data
=> Use linear regression

Split data -car stopped -car moving -fuel charged
and apply linear regression when the vehicle is moving.

3. Calculate Fuel Efficiency
 * instant Fuel Efficiency
 * Calculate Fuel Efficiency when the car is stopped
 * Calculate Fuel Efficiency when the fuel is charged
 * Overall Fuel Efficiency
 * Estimate the distance vehicle can travel with current Fuel level and Fuel efficiency

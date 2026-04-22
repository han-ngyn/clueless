# clueless
CS32 FINAL PROJECT: Han Nguyen and Esper Murray

Stuck on what to wear?? Don’t fret! Clueless has you covered with outfit planning technology that incorporates weather information, mood, and a little bit of magic to help you start your day off right.

To incorporate the mood component, we plan on associating the primary color of an article of clothing with a user chosen mood (from a list of moods). To achieve this, we will first use our knowledge of pixels to isolate the top 1 or 2 most prominent pixel colors in an image of a piece of clothing. The final outfit will include at least ONE article of clothing with the mood associated color as the most prominent color.

To incorporate the weather component, we will draw from weather app data and set a number of temperature thresholds that dictate what outfits are comprised of in terms of sleeve length, pant length, and whether or not a coat is worn. Thresholds would be hard coded and from here, we would have narrowed down what articles of clothing are eligible for being included in the final outfit. We can then go back to our color component and see what articles of clothing fit both parameters.

Finally, we will give the user a degree of choice and provide 3 potential outfits for the user to choose from.

At this point in time, we rely on the user determining the primary color of a given article of clothing. With this being the case, the instructions for a user are as follows.  
User Instruction:
Create a wardrobe csv file that includes necessary information about your wardrobe items. 
Be sure to follow the sample structure of item name, category, length, and color. 
From here, your clueless.py file will be able to access your wardrobe information and create the perfect weather matched, mood matched outfits for you. 
Feel free to edit or add to the provided mood_colors csv file if there are certain colors that resonate to different moods than previously indicated. This will allow for further personalization of your personal outfit picker!

Lastly, our python has now successfully incorporated connection to a local weather API so inputting the temperature is no longer necessary. Our code extracts the highest and lowest projected temperature of the day and takes the average of these numbers to ensure your outfit has you covered for the entire day. 

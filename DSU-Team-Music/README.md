# How does performing in music festivals impact up-and-coming electronic producers and DJs?
## The Data Science Union at UCLA - Team Music
Team Leader: Anton Citko

Team Members: Greyson Brothers, Louis Zhao, Tony Li, Sophie Yun

# Table of Contents
- [Summary](#summary)
- [Introduction](#introduction)
- [Data Collection](#data-collection)
- [Analysis](#analysis)
- [Conclusion](#conclusion)

# Summary

* For 30 different electronic producers and DJs we collected data on their music festival performances, song releases, and historical Spotify popularity metrics to determine how their festival performances impact their following.
* In general, we found that the rate at which they gained Spotify Followers and Monthly Listeners increased the week after a music festival compared to the week before. However, the increase in Monthly Listeners was more volatile than the increase in Followers.
* Using a fixed effects linear model, we found that the first two week following a music festival significantly increased the DJs rate of increase in Spotify Followers but not Monthly Listeners.
* This report confirms and quantifies the positive effect festival performances have on DJs careers by building a fanbase.

# Introduction
As music has become cheaper to consume through streaming services, music festivals have become a major source of income for them as they have grown in size, price, and production value. Electronic dance music has been at the center of this expansion. These festivals, like Electric Daisy Carnival and Tomorrowland, feature electronic producers and DJs from the top 100 charts to underground up-and-coming. Even though the popular DJs are the main draw for many, the smaller ones garner large audiences as well. For top DJs that have already become famous, the main drive to perform is financial, whereas up-and-coming use it to demonstrate their prowess at producing music and spinning behind the turntables. Exposure at the festivals leads audience members to discover amazing new acts. This leads us to wonder if it is possible to quantify the impact of these performances on a younger DJ’s popularity.

# Data Collection
To first determine which artists we should look into, we used previous lineups of several popular US festivals to create a list of potential individuals for analysis. After scraping Jambase for this list, we used Spotify’s API to find out their Monthly Listeners and Followers. Putting this together, we wanted to segment artists by these popularity metrics to determine which ones were up-and-coming. We used a cutoff of 150,000 followers. Additionally, this way a slight increase in following is easier to observe and measure. From there we sampled 30 artists to focus our analysis on.

Next, we scraped all necessary popularity and festival data for each of these 30 DJs. Festival dates and information data we were able to collect from Songkick’s gigography web pages. In addition to festival dates, we pulled song release date data for each artist using Spotify’s API. The release dates of songs will be important to control for in our analysis since we are measuring popularity in part through Spotify’s Monthly Listeners, which is driven by song releases. Finally we got the historical time series data for each DJs Monthly Listeners and Followers on Spotify. The distribution of these metrics, as well as the number of festival performances, for the selected artists can be seen below. It can be seen that there is a wide variety of electronic artists in popularity and number of performances.

![Number of Followers](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Number%20of%20Followers.png?raw=true)
![Number of Monthly Listeners](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Number%20of%20Monthly%20Listeners.png?raw=true)
![Number of Followers](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Number%20of%20Festivals.png?raw=true)

# Analysis
Our analysis began by trying to see if there were any patterns between when festivals occurred and how the popularity metrics changed. An example of this can be seen for Lil Texas below. Each graph has too much information to determine the impact of his music festival performances. Even though they are quite chaotic with festival and song release dates, they offer a couple insights about our data.

![Lil Texas Followers](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Lil%20Texas%20Followers.png?raw=true)
![Lil Texas Monthly Listeners](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Lil%20Texas%20Monthly%20Listeners.png?raw=true)

Firstly, followers have a clear, positive trend with only relatively small deviations from its general slope. Monthly Listeners has much more seemingly random changes. As we noted in these graphs and through some investigation for other artists, often times a hit single can garner an artist a large increase in listeners. The peak of the increase in listeners is usually temporary, lasting a few months, but can result in the artist having more listeners then before. After checking Spotify’s information on the metric, we learned that each unique listener increases the Monthly Listeners by one for 30 days, so this seems natural.

In order to understand the relationship between the number of music festivals an artist plays at and the change in following, we created a variable that measured the artists day to day change in Followers and Monthly Listeners. We then created scatter plots and a linear model for this metric. Even though the R2 was low, the number of music festival performances was a significant predictor for both average change in Followers and in Monthly Listeners. The relationship can be seen in the next two graphs.

![Festivals vs Change in Followers](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Festivals%20vs%20Change%20in%20Followers.png?raw=true)
![Festivals vs Change in Monthly Listeners](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Festivals%20vs%20Change%20Monthly%20Listeners.png?raw=true)

However, as can be seen in the initial bar plots in the data collection section, DJs that had a large number of Followers and Monthly Listeners also played in more festivals. So it appears we have a chicken, egg scenario, do more popular artists play in more music festivals or is it the number of music festivals that makes them more popular? The following graphs show that there is a clear relationship between the number of music festival performances and their overall average Followers and Monthly Listeners.

![Festivals vs Followers](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Festivals%20vs%20Followers.png?raw=true)
![Festivals vs Monthly Listeners](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Festivals%20vs%20Monthly%20Listeners.png?raw=true)

Even though it would be difficult to determine the lead and lag in this relationship, we can see in the linear model information here that the average number of total followers does a much better job at predicting the average change in followers than the number of festivals that the DJs performed at. That tells us that generally artists with more followers will have larger changes in the number of followers that they have. This makes sense because of scale. A DJ with 100,000 followers might garner 10,000 new followers in a month whereas a DJ with 10,000 followers garnering 10,000 new followers would be much more unlikely.

![Average Follower Change Linear Model Summary](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Average%20Follower%20Change%20Linear%20Model%20Summary.png?raw=true)

To control for this, we created a percent change metric to measure the change in Monthly Listeners and Followers. This way a DJ with 100,000 followers increasing its following by 10,000 and a DJ with 10,000 followers increasing its following by 1,000 would both be measured as having increased their following by 10%. The two graphs below show that the relationship between number of festival performances and percent growth in followers are not correlated. This leads us to believe that larger artists simply perform in more music festivals but that they also garner relatively the same increases in following as smaller artists.

![Festivals vs Followers](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Festivals%20vs%20Followers.png?raw=true)
![Festivals vs Followers](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Festivals%20vs%20Followers.png?raw=true)

Rather than focusing on the number of festivals, we can measure the change in popularity for each artist before and after playing in a music festival. The graph on the left below shows the average percent change of followers for each artist in the week leading up and following a music festival performance. It can be seen that the week before, in grey, tends to be less than the week after, in orange. Looking at it another way, the graph on the right shows that the week after averaged a higher percentage increase in followers than the week before for all but three artists. The average increase was 0.017.

![Dumbbell Followers](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Dumbbell%20Followers.png?raw=true)
![Change in Growth Rate Followers](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Change%20in%20Growth%20Rate%20Followers.png?raw=true)

Conducting the same analysis on monthly listeners reveals that the average increase was 0.018. However, the graphs below reveal the increase was far more inconsistent. The standard deviation for the change was 0.322 whereas the standard deviation for the change in percent followers growth is 0.0457, which means that we cannot say this increase is significantly different from zero. Furthermore, we noticed in general that monthly listeners had much more variation in its percent change than followers.

![Dumbbell Monthly Listeners](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Dumbbell%20Monthly%20Listeners.png?raw=true)
![Change in Growth Rate Monthly Listeners](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Change%20in%20Growth%20Rate%20Monthly%20Listeners.png?raw=true)

In order to determine whether the increase was significant, we created a fixed effects linear model. This would take into account the differences between artists. Essentially, if one artist has had a stellar last few years the model would attempt to control for that so we can focus on the change in followers before and after the festival. Additionally, we added in the effects of the weeks after a song was released. Based on the output here, the first week after the festival has the strongest increase in follower percent change of 0.020. The second week has a smaller effect of 0.013 and the third week is not significant. It is also notable that the first week after a song is released has only a slightly higher increase in followers than the first week after a festival performance (0.024 vs. 0.020). We conducted the same analysis for monthly listener percentage change but it was not significant for the weeks following the festival.

![Fixed Effects Model Summary](https://github.com/AntonCitko/DSU-Team-Music/blob/master/Visualizations/Fixed%20Effects%20Model%20Summary.png?raw=true)

# Conclusion
Our analysis revealed that festival performances indeed have a significant impact on artists ability to garner followers on Spotify. The impact of this effect lasts for about two weeks after the music festival. The first week after increases the percent change in followers by 0.020 and the second week increases it by 0.013. To put this in perspective, Andrew Bayer’s effect in the model was 0.067 and averaged 42992 total followers. So, without having released a song or playing in a music festival in a couple of weeks he averaged 29 new followers each day. If we factor in the effect of playing in a music festival, his percent change in followers for the week after would increase by 0.020. Thus, for each day in that week after the music festival he would average a gain of 37 followers each day instead of his average 29.

Even though we see noticeable gains in followers, we do not see a significant increase in monthly listeners in the weeks following a music festival performance. This is likely because monthly listeners is typically about ten times higher than followers, so a couple dozen followers is far more noticeable and impactful than the same increase in monthly listeners.

Success as a musician in the digital world can be measured in a number of different ways. Monthly Listeners on Spotify directly measures how many unique people listen to an artists music and these listens determine how much money Spotify pays them. Followers only tells us how many people clicked follow on the artist's Spotify page and does not tell us how much money they get paid by Spotify. But, we would surmise that followers tend to be the ones that go to an artist’s performances, buy merchandise, and listen to songs multiple times. So, playing at a music festival will not vastly increase an artist’s reach but help fans discover them.

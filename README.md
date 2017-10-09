# rightscale-plugin-costs

#### Summary
I've started writing some *kinda* all-in-on Python scripts that let you create/modify/remove custom [plugin costs in RightScale Optima](http://reference.rightscale.com/cloud_analytics/analytics_api/index.html#/1.0/controller/V1-ApiResources-PluginCosts). Why tho? Well, say you currently use Optima as your single source of truth for all your *cloudy* costs but still have to go to some other means to work out your non-IaaS/cloud provider costs. For example consultancy costs or some other billable time, usage based services usually SaaS, or maybe some other completely random source of costs that you just want to throw into Optima because you can. 

#### How to use the scripts
So first of all I assume you're using MacOS or Linux and you have Python installed. If you're using Windows you should hit up [bash for Windows]( https://msdn.microsoft.com/en-au/commandline/wsl/about) or maybe spin up an Alpine container with Docker. There's probably an easier way to get Python on Windows but I haven't Googled it yet.

Download the script or scripts you would like based on their title which explains what they do. Edit the scripts and change the variables you need to change eg `my-refresh-token`. Then open a terminal and type `python <script-name>.py`. That's it! If you ran the `create-cost-plugin.py` script you should now see the UI in Optima ([example](https://i.imgur.com/z58NJNB.png)).

Please PR if you feel like contributing and fixing up my *"work"*.

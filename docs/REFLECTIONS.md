# Lessons Learned

These are the lessons I picked up while working on this project. Some came from researching a question I had, while others only clicked after I tested things and saw the results.

1. **TWhy tag an image with the Git SHA**

   Tagging an image with the git SHA helps you know which commit the image corresponds to.
   tagging an image with `latest` is convenient, but it doesn't tell you which commit the image corresponds to.
   If a problem arises, it can help you connect the image running to the code that produced it and help you narrow down which changes might have introduced the problem.  


2. **`$GITHUB_SHA` vs. `${{ github.sha }}`**

   Both gives the commit SHA for the workflow run, but they come from different places. `$GITHUB_SHA` is an environment variable provided by GitHub Actions, so I can use it directly in a shell command inside a `run` step. `${{ github.sha }}` is a context expression evaluated by GitHub Actions. They give the same value, just through different mechanisms. In Bash, you can reference the environment variable as `$GITHUB_SHA` inside a `run` command. GitHub explains both in its [variables and contexts documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/variables).

3. **Don't guess CPU and memory limits**

   The task required configuring CPU and memory limits, so I had to figure out how much to allocate. How do you decide or know before hand just how much to allocate so you don't overprovision or underprovision resources?
   The way to do this is by monitoring the resource usage before allocating resources for your workload.
   I used `docker stats` while testing the application to monitor its resource usage. That gave me a starting point, but monitoring over time and under realistic workloads matters too. For more advanced monitoring, options include Prometheus with Grafana, or Telegraf with InfluxDB.

4. **“It works on my machine” isn't a guarantee**

   After testing the app, I set its memory limit to the minimum it needed to run. It worked on my machine, so I thought I had found the right limit. Then I ran the same setup in WSL on my PC, a VirtualBox VM, and an EC2 instance. WSL and the VM ran without an out-of-memory error, but EC2 hit OOM almost immediately. Oddly, the health check timed out on my PC but passed in the VM and on EC2. Increasing the memory limit and health-check timeout resolved the issues.

   That was the point where my 'works on my machine' assumption fell apart. I'd assumed that packaging an application and its dependencies in containers meant it would behave the same everywhere. Not quite. 
   
   You see, containers are Linux processes, and their performance and behavior can still be very much influenced by the underlining hardware running these processes.

   So, while docker grants you the portability and flexibility of running applications in different environment, you still need to take into account the adjust for the different environments your application would run and not configure unnecessary and arbitrary (just because it works on my machine) limits and constraints.
   
   In addition, memory limits should not be set to the minimum possible value, but always configure buffers to account for unknown and random events.

   
5. **Do actions make a workflow faster than `run` commands?**

   This started with a question: would using an action instead of a `run` command make my pipeline faster? After looking into it, I realised neither option is automatically faster. What matters is what I want to accomplish. 

   I  don't need to hide every pipeline logic behind an action. A `run: pytest` or `run: flake8` step makes it easy to see what's happening. Actions are useful when a task has substantial setup, needs to be reused, or can be handled by a reliable existing action.

6. **One step or several?**

   I also wondered whether putting several commands in one step would be faster than splitting them into separate steps. 
   
   I realised that fewer steps don't automatically mean a faster workflow. Separate steps make logs easier to follow and give a clearer control over conditions, timeouts, and failures. GitHub's [workflow syntax documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) explains the controls available for individual steps.
   
   It is helpful to keep related commands together when that makes sense, but you don't need to always bundle everything into one step.

7. **What to test**

   The first test I wrote was quite cumbersome. 
   I was  testing every little implementation detail, including whether `lpush` and `hset` were called. I kept running into mocking and
   patching issues while running the implementation. Although, working through these challenges helped me better understand these concepts, I started wondering how much testing code I would have to write when working with large codebase and if it made sense writing so much code for test.
   
   I did some reading and came across a the correct approach when testing: **test the behavior, not every implementation detail.**
   
   Instead of checking every method call, check that the code produces the expected result. 
   
   [This article on practical testing](https://martinfowler.com/articles/practical-test-pyramid.html) helped me understand why tests shouldn't be tied too closely to implementation details and how to decide what to test.

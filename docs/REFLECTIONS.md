# Lessons Learned

These are the lessons I picked up while working on this project. Some came from researching a question I had, while others only clicked after I tested things and saw the results.

1. **TWhy tag an image with the Git SHA**

   Every commit in git has a unique hash, like a3f9c2e1... (40 characters). GitHub exposes the current commit's hash to your workflow as an environment variable called GITHUB_SHA. 

   A Docker tag is just a label pointing at an image. If you only ever push myapp:latest, every build overwrites the same label — you lose the ability to say "which code is actually running in production right now?" or "roll back to yesterday's build." Tagging with the SHA gives every image build a unique, permanent, traceable name tied to the exact code that produced it. latest is just a convenience pointer that always floats to the newest one — nice for local dev, useless for auditing or rollbacks.


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

   
5. **Using an action versus using a `run` command?**

   This started with a question that came to mind: would using an action instead of a `run` command make my pipeline faster? After looking into it, I realised that using an action isn't necessarily faster.  
   
   Pipeline performance is rather dependent on:
   - dependency download time
   - use of caching
   - runner startup time
   - tool installation time e.t.c.

   Also, you don't need to hide every pipeline logic behind an action. A 
   `run: pytest` or `run: flake8` step makes it easy to see what's happening. 
   
   Actions are useful when a task has substantial setup, needs to be reused, or can be handled by a reliable existing action.

6. **One step or several?**

   I also wondered whether putting several commands in one step would be faster than splitting them into separate steps. 
   
   I realised that fewer steps don't automatically mean a faster workflow. Although, separate steps make logs easier to follow and give a clearer control over conditions, timeouts, and failures. GitHub's [workflow syntax documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) explains the controls available for individual steps.
   
   It is helpful to keep related commands together when that makes sense, but you don't need to always bundle everything into one step.

7. **What to test**

   Heck, in my initial test I was testing every line, ensuring lpush and hset was called. Started experiencing some monkey patching and mock issues that almost turned me into a monkey. phew!
   Although, I did get some needed clarification on my understanding of monkeypatching, patching, and mocking.  
   I guess the realisation came to me when I realised how much I would need to write if I was working on a large codebase and if this actually made sense. 
   
   This prompeted me to do some research, and I realised some principles that helped me write better tests.
   Here's a cool article on testing I found helpful should you decide to
   [dig deeper](https://martinfowler.com/articles/practical-test-pyramid.html?utm_source=chatgpt.com)

   The principles:
   1. Test behavior, not implementation:
   The test should help understand what the function is supposed to do
   even without knowing how it should be implemented.

   Per the [pytest docs](https://docs.pytest.org/en/stable/explanation/anatomy.html): "But exactly how or why something is done is not quite as important as what was done." 

   2. You don't need a test for every line
   
   3. A good rule of thumb: Every meaningful if, else, exception path, or alternative outcome deserves consideration.

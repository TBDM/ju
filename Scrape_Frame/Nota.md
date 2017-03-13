##Issues

+ 1. [FIN] task['fail'] needs to be added, no longer parsing from time.
+ 2. [FIN] the filename saved should be distinguished for the same page scraped at the same day, avoiding over-writing.
+ 3. remove the useless scripts in saved pages to reduce filesize.
+ 4. [FIN - need IMPR] build special rules for activities and special ju banners.
+ 5. [FIN] penality time should be based on now_time for 1st time scrape.
+ 6. [FIN - OBSV] **check the logic of removing .lock file.**
+ 7. [FIN] don't use += for penality time!
+ 8. [FIN] several coding issues with Ubuntu-env, do check.
+ 9. [FIN] Add at least 30 secs for Pipe-tasktime-halting.
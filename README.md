The current configuration of this project:

# Datasette

*hipaabreach.db*
* table `breach_report` - capture of the csv for announced but unresolved hipaa breaches
* table `breach_report_archive` - capture of the separate csv for breaches with non-empty "Web Description," which details the final outcome of a hipaa breach investigation, including details for remediation and/or mitigation plans
* `ransomware` in hipaabreach.db - view created from keyword search for "ransomware" (viewable in datasette, integrates both tables)
* foreign key on Covered Entity, which shows up as a hyperlinked name on `breach_report` to `breach_report_archive`; established to identify repeat offenders but mostly turns up 404 errors that show there aren't really repeat offenders (limited value, informed Future State plan below)

# Slack Bot

*bot.py*
* draws **n** rows from `breach_report` for most recently announced breaches
* draws **n** rows from `breach_report_archive` for breaches with recently announced action / mitigation agreements
* draws **n** rows from ransomware view to highlight most recent ransomware investigation for further reporting; noting here that 'Web Description' details do not seem to include resolution to the effect of "yeah, we paid the bribe to get our data back" -- requires further reporting

*slack message content*
Three alerts that respond to the following use cases:

1. As a reporter, I want to see the latest breach submission(s) so that I can assess them for news value. Hence, the contents of the slack message include the key data -- name of the "covered entity," aka hospital, medical provider, vendor; number of people affected; submission date.

2. As a reporter, I want to see the details of any settlement between a covered entity and HHS in order to assess its news value, determined by:
* fines assessed?
* remediation proportional to people affected?
* sizable gap between breach submission date and detection (where detection date often included in 'Web Description' content sent to slack) as an indicator for how long the bad guys may have had access to data?

Hence, the slack message contains the name of the covered entity, the original submission date, and all details available from this data source about the resolution. This should answer the threshold question: Do I need to start making calls?

3. As a reporter, I want to see the latest resolution of any case involving ransomware, because news. More on this below.

# Future State

The final version of this project would ideally do the following:

Datasette:
* instantiate an empty database that establishes a primary key for each breach (Covered Entity + Submission Date at minimum)
* upsert the breach submission data (breach_report.csv)
* upsert the breach resolution data (breach_report_archive.csv) to the same table so that individual reports can be tracked as an "update" to the table as opposed to a new add to the 'archive' database
* refresh the data feed with an upsert approximately daily (see below)
* automatically refresh the ransomware view with each update, instead of recreating manually (creating a db view seems more useful than, for example, creating canned SQL to search for the keyword 'ransomware,' if for no other reason than to facilitate robots taking over the ransomware alert job)  

Bot:
* reconfigure slack bot to identify new-and-not-already-flagged additions of breach submissions
* reconfigure slack bot to identify any row where Web Description changes from an empty string to having content, thereby announcing a breach resolution
* flag recent ransomware -- this needs a little research, since I believe the view needs to be created from scratch; it's possible that the item directly above could be flagged with something like the slack :pirate_flag: if the word "ransomware" is detected?

**Should this bot accept input from users?**
 Contemplating the likely use cases, I'm leaning to answering this question as "no" unless a user wants to query slack for the 'Web Description' details instead of having them sent in the alert message.
 If yes, I'd envision a system where the slack message says something like, "type 'details' for more information" and upon getting 'details', the slackbot would send the text contained in 'Web Description'. However, as a user, I think this would get tiresome and I'd just want the details sent the first time.
 Possible outcomes:
 * a user might want to answer questions from querying slack, in which case, those questions would need to be refined
 * a user might go straight to the datasette app (more likely imho) for further research, in which case some canned sql might get to an  answer with a wider perspective faster than using slack to mediate

 **What's the best schedule for updates?**
 The simplest answer is daily. It would be worth a week or two of manual monitoring to see whether the breach announcements get posted at roughly the same time daily, or more than once a day, to optimize the update schedule.


# CFAnalyze -- Just Simple CloundFront Access Log Analyzer

## Usage

 
        $ cfa -b log-bucket -t referer --after 2012-09-19 log_prefix
        
## Output Example

        $ cfa -b log-bucket -t referr --after 2012-09-19 log_prefix
        50768	http://gae9.com/
        9925	-
        9665	http://gae9.com/gag/170
        8871	http://gae9.com/?sort=new
        7900	http://gae9.com/gag/165
        6157	http://gae9.com/?
        …
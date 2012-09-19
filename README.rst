CFAnalyze -- Just Simple CloundFront Access Log Analyzer
========================================================

Usage
-----

::

    $ cfa -b log-bucket -t referer --after 2012-09-19 log_prefix
        
Output Example
--------------

::

    $ cfa -b log-bucket -t referer --after 2012-09-19 log_prefix
    50768 http://gae9.com/
    9925  -
    9665  http://gae9.com/gag/170
    8871  http://gae9.com/?sort=new
    7900  http://gae9.com/gag/165
    6157  http://gae9.com/?
    …

    $ cfa -b log-bucket -t content_traffic --after 2012-09-19 log_prefix
    URL                                                                               Bytes(MB)        Hit
    /assets/new/js/jquery.cookie-0817b5d2.js                                              18.33      12779
    /assets/new/css/bootstrap.min-9a067c55.css                                            58.84       6610
    /assets/new/css/style-cb2fc518.css                                                    5.089       6310
    /assets/new/js/common-0de56a47.js                                                     22.11       6045
    /assets/new/img/glyphicons-halflings-84f6138b.png                                     51.83       5683
    /d729f370da484ad38c015b86dc3f1aa7.thumb.jpg                                           159.3       5244
    /d7eaf3d721814e1f9ea632799ea63475.thumb.jpg                                           12.27       3083
    ...
    Grand Total:
    Hit: 120,215
    Bytes(MB): 5,431

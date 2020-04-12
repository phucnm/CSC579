# CSC579

An Analysis of HTTP/2: The present and the future.

[Project proposal](proposal.md)

[Literature review](servers_adoption.md)

[Project presenation](https://drive.google.com/open?id=1gPxkHytO-3c1vs1pzGRvDawIHncJc_2B)

Final report: [Final report](HTTP2_Analysis_2.pdf)

The Alexa top 1m websites can be found [here](http://s3.amazonaws.com/alexa-static/top-1m.csv.zip). However there are only ~700k websites.

For the adoption examination, we wrote a program in Python to check the HTTP/2 support status of Alexa top 511,850 websites. All websites are sorted by rank in a csv file. Each line contains two parts separated by a comma: the rank of the site and its domain without http schema prefix (http:// or https://) e.g. facebook.com, google.com. The program uses nghttp2 command-line interface (CLI) to send and receive HTTP/2 requests. nghttp2 is one of the most efficient and mature HTTP/2 implementations \cite{nghttp2}. Responses from websites are in form of strings. We obtain useful fields of this data using regular expressions, and then store results in a sqlite database for further analysis. 

We use ThreadPool in Python to speed up the experiment up to 5 requests/s. It means that it takes nearly 28 hours and 25 minutes to complete requesting all the sites. Not to mention when the Internet is unstable or the website is unreachable, we need to query failed sites in the database and run the tool again for those sites.

A lot of sites do not handle unknown HTTP protocols in the handshake phase. It caused the tool wait for several minutes to get an error response. To avoid this, we added a timeout 5s to nghttp command. There is a trade-off by doing this, for some sites, they responses the whole web page content and the end to end latency may be longer than 3s. If the timeout is large, it takes much more time to finish the experiment.

# Project Proposal

## Title: An analysis of HTTP/2: The present and the future.

### Overview

Since the first introduction of HTTP in the early 90's, HTTP has became the most common data communication protocol used by the World Wide Web. Many tweaks were implemented to resolve issues and improve the protocol, but the core implementation remain unchanged. As websites become more and more complicated, clients need a longer time to load web pages, thus reduce overall user experience. In an attempt to replace HTTP, Google built an experimental procotol called SPDY [1] in 2009 with the focus was to reduce web page load latency through compression, multiplexing and prioritization. In 2015, the Internet Engineering Task Force (IETF), who maintains the HTTP, developed HTTP/2 [2] largely based on the SPDY project. HTTP/2 addresses several limitations in HTTP as well as enhance the protocol's simplicity, performance and robustness. HTTP/2 inherits all advantages from SPDY, and was improved in many aspects including but not limited to encryption, compression during its development. 

Although HTTP/2 solves several issues of the predecessor, it is severly affect by packet loss due to TCP congestion control. Basically, TCP waits for the lost packets to be resent and fill the gaps in the byte stream. This is one of reasons leads to QUIC [3] which is based on top of UDP and HTTP/3 proposals whereas HTTP/2 is not yet fully adopted.

Because HTTP is widely used, adoption of HTTP/2 takes time. In addition, the adoption must come from both sides: server side (web servers, CDNs) and client side (desktop web browers, mobile web browsers) According to W3Techs [], as of Jan 2020, 42.9% of the top 10 million websites supported HTTP/2 [4]. 

### Methodologies

In this project, we want to provide a comprehensive study about HTTP/2 current adoption, advantages features compared to HTTP (protocol negotiation, performance, security) and its future development direction. More specifically, for adoption analysis, we gather adoption data from multiple sources to show a complete adoption history of HTTP/2 since its standardization in 2015. For performance, we collect HTTP/2 performance benchmarks to provide an objective point of view on HTTP/2 performance improvements in comparison to with HTTP. We also investigate whether security is enhanced in HTTP/2. For HTTP/2 development direction, we discuss its future where there is a proposal for HTTP/3 and the appearence of Google's QUIC - an entirely new web protocol on top of UDP.

### Tentative schedule

Jan 31 - Project proposal

Feb 14 - Data Collection

Feb 28 - Report writing

Mar 13 - Revision

Mar 27 - Final report & Presentation


### References

[1] SPDY: An experimental protocol for a faster web, https://www.chromium.org/spdy/spdy-whitepaper (accessed on Jan 31 2020)

[2]  Hypertext Transfer Protocol Version 2 (HTTP/2), https://tools.ietf.org/html/rfc7540 (accessed on Jan 31 2020)

[3] Langley et al., The QUIC Transport Protocol: Design and Internet-Scale Deployment.

[4] Usage statistics of HTTP/2 for websites, https://w3techs.com/technologies/details/ce-http2 (accessed on Jan 31 2020)

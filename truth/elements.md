# Ground truth elements

**Status:** FROZEN PRE-RUN YARDSTICK — exact Tier column human-signed-off and tagged before any model run.
**Source length:** 3,284 lines / approximately 32,000 words.
**Inventory provenance:** ChatGPT produced the initial end-to-end inventory from `design.md`; no prompt variant or model output under test was opened.
**Human review:** Liban m stated on 2026-07-12 that he read the pre-tier inventory end to end and reviewed its inclusion, exclusion, line-reference, and ambiguity decisions.
**Tiering provenance:** ChatGPT applied the human-specified tiering rule below; Liban m reviewed and signed off the exact Tier column on 2026-07-12 after the risk-centric rule was made explicit and P1 (the servlet container/Tomcat) was corrected to CORE.
**Burial labels:** `STATED PLAINLY` means named directly and difficult to miss; `BURIED` means a competent person skimming for architecture could plausibly miss it.

## Review sign-off

| Review item | Reviewer | Date | Status |
|-------------|----------|------|--------|
| End-to-end inventory, inclusions/exclusions, line references, and ambiguity notes | Liban m | 2026-07-12 | SIGNED OFF — reviewer explicitly stated the pre-tier inventory was read end to end |
| CORE/EXTENDED decision rule and compact approximately-30-row CORE target | Liban m | 2026-07-12 | SIGNED OFF — supplied by the reviewer before any model run |
| Exact CORE/EXTENDED assignment on each row | Liban m | 2026-07-12 | SIGNED OFF — approved after the risk-centric tiering rule was stated explicitly and P1 was moved to CORE |

## Tiering and scoring

- **CORE** is the canonical set any competent threat model of this system must cover: the architecture spine, principal trust boundaries, authentication/configuration stores, credential-bearing connection data, tunnels, plugins, reverse proxy, database, and the plaintext-by-default web-application-to-`guacd` hop.
- **EXTENDED** is real and present in `design.md`, but optional, peripheral, protocol-specific, operational, or a finer-grained duplicate of a CORE concept. A row may therefore be EXTENDED even when it elaborates a concept represented by another CORE row.
- **Risk-centric assignment rule:** risk-bearing stores, flows, and trust-boundary crossings are CORE; interchangeable provider, driver, or helper processes that merely operate them are EXTENDED unless the process itself forms part of the architecture spine. Thus `user-mapping.xml` is CORE while the XML authentication provider is EXTENDED, and the JDBC database/flow/boundary are CORE while the database authentication extension and JDBC driver are EXTENDED. The servlet container is CORE because it hosts the web application and terminates the proxied application path; the reverse proxy remains CORE because it defines the public TLS-termination and client-network boundary when deployed.
- The headline coverage result is calculated against **CORE only**. **EXTENDED** coverage is reported separately as a secondary result and must not be folded into the headline score.
- This frozen version contains **31 CORE rows** and **108 EXTENDED rows**. Any later change requires a new yardstick version, an explicit row-level change log, and rerunning all arms; it must not be applied retroactively.


## External entities

| ID | Tier | Element | Where it appears in design.md | Stated plainly or buried? |
|----|------|---------|-------------------------------|---------------------------|
| E1 | CORE | End user / Guacamole user | `design.md:L17`, `design.md:L45` | STATED PLAINLY |
| E2 | EXTENDED | User web browser | `design.md:L17` | STATED PLAINLY |
| E3 | CORE | Generic remote desktop server / destination machine | `design.md:L19`, `design.md:L75` | STATED PLAINLY |
| E4 | EXTENDED | VNC server | `design.md:L358-L364` | STATED PLAINLY |
| E5 | EXTENDED | VNC repeater / VNC proxy, such as UltraVNC Repeater | `design.md:L409-L417` | BURIED |
| E6 | EXTENDED | PulseAudio server on or near the VNC host | `design.md:L433-L464` | BURIED |
| E7 | EXTENDED | RDP server / Windows remote desktop host | `design.md:L563-L577` | STATED PLAINLY |
| E8 | EXTENDED | Microsoft Remote Desktop Gateway | `design.md:L901-L918` | BURIED |
| E9 | EXTENDED | RDP load balancer / connection broker / TS session broker | `design.md:L922-L929` | BURIED |
| E10 | EXTENDED | Hyper-V / VMConnect host and destination virtual machine | `design.md:L870-L897` | BURIED |
| E11 | EXTENDED | SSH server | `design.md:L1037-L1048` | STATED PLAINLY |
| E12 | EXTENDED | SFTP server / remote SFTP filesystem | `design.md:L1108-L1126`, `design.md:L1331-L1382` | BURIED |
| E13 | EXTENDED | Telnet server | `design.md:L1172-L1200`, `design.md:L1228` | STATED PLAINLY |
| E14 | EXTENDED | Kubernetes API server, namespace, pod, and container | `design.md:L1230-L1234`, `design.md:L1256-L1299` | STATED PLAINLY |
| E15 | CORE | JDBC database server: MariaDB, MySQL, PostgreSQL, or SQL Server | `design.md:L1819-L1831` | STATED PLAINLY |
| E16 | EXTENDED | External identity systems: CAS server and LDAP server; OpenID/SAML providers are also named | `design.md:L177-L180`, `design.md:L1634-L1650` | BURIED |
| E17 | EXTENDED | Remote host, router, broadcast domain, or multicast group receiving Wake-on-LAN packets | `design.md:L1565-L1586` | BURIED |
| E18 | EXTENDED | Reverse proxy edge, implemented with Nginx or Apache | `design.md:L3028-L3032`, `design.md:L3088-L3090`, `design.md:L3175-L3179` | STATED PLAINLY |
| E19 | EXTENDED | Additional upstream proxies or firewalls between clients and the trusted reverse proxy | `design.md:L3061-L3063` | BURIED |
| E20 | CORE | Administrator using the web-based administrative interface or SQL directly | `design.md:L257`, `design.md:L1821`, `design.md:L2544-L2548` | STATED PLAINLY |

## Processes

| ID | Tier | Element | Where it appears in design.md | Stated plainly or buried? |
|----|------|---------|-------------------------------|---------------------------|
| P1 | CORE | Web server / Java servlet container, commonly Tomcat | `design.md:L17`, `design.md:L49`, `design.md:L212`, `design.md:L3036-L3053` | STATED PLAINLY |
| P2 | CORE | Browser-resident Guacamole JavaScript client | `design.md:L17`, `design.md:L45` | STATED PLAINLY |
| P3 | CORE | Guacamole Java web application | `design.md:L19`, `design.md:L43-L49` | STATED PLAINLY |
| P4 | CORE | Web-application authentication layer and extension framework | `design.md:L47`, `design.md:L253-L257` | BURIED |
| P5 | EXTENDED | Default XML authentication provider | `design.md:L84`, `design.md:L253-L263` | STATED PLAINLY |
| P6 | EXTENDED | Database authentication extension | `design.md:L1819-L1823`, `design.md:L2088-L2108` | STATED PLAINLY |
| P7 | CORE | `guacd` native proxy daemon | `design.md:L31-L39` | STATED PLAINLY |
| P8 | CORE | `libguac` shared library used by `guacd` and every client plugin | `design.md:L39`, `design.md:L73` | BURIED |
| P9 | CORE | Dynamically loaded client plugins, which run independently of `guacd` once loaded | `design.md:L35-L39` | BURIED |
| P10 | EXTENDED | Protocol client libraries: `libguac-client-vnc`, `-rdp`, `-ssh`, `-telnet`, and `-kubernetes` | `design.md:L340`, `design.md:L547`, `design.md:L1005`, `design.md:L1150`, `design.md:L1234` | BURIED |
| P11 | EXTENDED | Server-side terminal emulator used by SSH, Telnet, and Kubernetes support | `design.md:L1003`, `design.md:L1148`, `design.md:L1232`, `design.md:L1510` | BURIED |
| P12 | EXTENDED | Guacamole WebSocket tunnel handler | `design.md:L67`, `design.md:L3206-L3224` | BURIED |
| P13 | EXTENDED | Guacamole HTTP fallback tunnel handler | `design.md:L67`, `design.md:L3179`, `design.md:L3274-L3276` | BURIED |
| P14 | CORE | Reverse proxy process, Nginx or Apache/mod_proxy | `design.md:L3030-L3032`, `design.md:L3088-L3112`, `design.md:L3175-L3202` | STATED PLAINLY |
| P15 | EXTENDED | Tomcat `RemoteIpValve` | `design.md:L3057-L3073` | BURIED |
| P16 | EXTENDED | Logback logging framework within the web application | `design.md:L103-L104`, `design.md:L229-L247` | BURIED |
| P17 | EXTENDED | JDBC driver loaded by the web application | `design.md:L1841-L1843`, `design.md:L2094-L2096` | BURIED |
| P18 | EXTENDED | GhostScript (`gs`) used to convert redirected RDP print jobs to PDF | `design.md:L801`, `design.md:L818-L821` | BURIED |
| P19 | EXTENDED | `guacctl` utility running on an SSH server to control uploads/downloads | `design.md:L1110-L1113` | BURIED |
| P20 | EXTENDED | `guacenc` recording-to-video conversion utility | `design.md:L1386-L1396` | BURIED |
| P21 | EXTENDED | `guaclog` key-event interpretation utility | `design.md:L1398-L1404` | BURIED |
| P22 | EXTENDED | Web-based administration interface for users, connections, permissions, and database-backed configuration | `design.md:L257`, `design.md:L1821`, `design.md:L2536-L2540` | STATED PLAINLY |
| P23 | EXTENDED | Connection-group balancing, failover, and session-affinity logic | `design.md:L2789-L2797`, `design.md:L2887-L2912` | BURIED |
| P24 | EXTENDED | Parameter-token substitution and parameter-prompting logic | `design.md:L1590-L1614`, `design.md:L1666-L1676` | BURIED |

## Data stores

| ID | Tier | Element | Where it appears in design.md | Stated plainly or buried? |
|----|------|---------|-------------------------------|---------------------------|
| D1 | CORE | `GUACAMOLE_HOME` configuration directory, `/etc/guacamole` by default | `design.md:L92-L98` | STATED PLAINLY |
| D2 | CORE | `guacamole.properties`, including `guacd` location/TLS settings, database credentials, and extension settings | `design.md:L100-L101`, `design.md:L126-L136`, `design.md:L184-L206`, `design.md:L2106-L2182` | STATED PLAINLY |
| D3 | CORE | `user-mapping.xml`, containing usernames, password material, connections, remote host parameters, and connection credentials | `design.md:L84`, `design.md:L261-L322` | BURIED |
| D4 | EXTENDED | `logback.xml` web-application logging configuration | `design.md:L103-L104`, `design.md:L229-L245` | BURIED |
| D5 | EXTENDED | `GUACAMOLE_HOME/extensions/` extension JAR store | `design.md:L106-L107`, `design.md:L2090-L2095` | BURIED |
| D6 | EXTENDED | `GUACAMOLE_HOME/lib/` shared-library and JDBC-driver store | `design.md:L109-L110`, `design.md:L1843`, `design.md:L2092-L2096` | BURIED |
| D7 | EXTENDED | `guacd.conf` daemon configuration file | `design.md:L1680-L1710` | STATED PLAINLY |
| D8 | EXTENDED | `guacd` PID file, commonly `/var/run/guacd.pid` | `design.md:L1690-L1693`, `design.md:L1747-L1750` | BURIED |
| D9 | EXTENDED | `guacd` TLS certificate and private key files | `design.md:L1700-L1708`, `design.md:L1769-L1775` | BURIED |
| D10 | EXTENDED | `ssh_known_hosts` in `GUACAMOLE_HOME` and per-connection host-key values | `design.md:L1027-L1033`, `design.md:L1047-L1050` | BURIED |
| D11 | EXTENDED | PulseAudio network configuration, usually `/etc/pulse/default.pa` | `design.md:L439-L447` | BURIED |
| D12 | EXTENDED | Web-application console/file logs, including Tomcat `catalina.out` | `design.md:L210-L212` | BURIED |
| D13 | EXTENDED | `guacd` syslog and foreground-console logs | `design.md:L1747-L1755`, `design.md:L1796-L1799` | BURIED |
| D14 | EXTENDED | RDP redirected-drive `drive-path`, which persists transferred files on the Guacamole server | `design.md:L803`, `design.md:L828-L856` | BURIED |
| D15 | EXTENDED | Graphical session-recording directory containing Guacamole protocol dumps | `design.md:L1386-L1389`, `design.md:L1411-L1439` | BURIED |
| D16 | EXTENDED | Human-readable key-event log generated by `guaclog` | `design.md:L1398-L1404` | BURIED |
| D17 | EXTENDED | Typescript recording directory containing raw terminal text and `.timing` files | `design.md:L1443-L1468` | BURIED |
| D18 | EXTENDED | Remote SFTP filesystem exposed through the Guacamole file browser | `design.md:L1110-L1124`, `design.md:L1331-L1382` | BURIED |
| D19 | CORE | Guacamole JDBC database as a whole | `design.md:L1922-L1928` | STATED PLAINLY |
| D20 | EXTENDED | Database entity and user records, including salted password hashes, salts, status, access windows, and user profile data | `design.md:L2552-L2567`, `design.md:L2571-L2635` | STATED PLAINLY |
| D21 | EXTENDED | `guacamole_user_password_history` | `design.md:L2667-L2694` | BURIED |
| D22 | EXTENDED | `guacamole_user_history` login/logout audit history | `design.md:L2698-L2720` | BURIED |
| D23 | EXTENDED | User groups and group membership: `guacamole_user_group` and `guacamole_user_group_member` | `design.md:L2724-L2750` | BURIED |
| D24 | CORE | Connections and arbitrary connection parameters, including remote credentials and per-connection `guacd` encryption choice | `design.md:L2754-L2808` | STATED PLAINLY |
| D25 | EXTENDED | `guacamole_connection_history` connection-usage audit history | `design.md:L2824-L2855` | BURIED |
| D26 | EXTENDED | Sharing profiles and parameters | `design.md:L2859-L2883` | BURIED |
| D27 | EXTENDED | Connection groups, balancing metadata, failover flags, and session-affinity settings | `design.md:L2887-L2912` | BURIED |
| D28 | EXTENDED | System, user, group, connection, sharing-profile, and connection-group permission tables | `design.md:L2922-L3023` | BURIED |
| D29 | EXTENDED | JDBC TLS trust stores, client certificate stores, PEM certificates, and private-key files | `design.md:L2245-L2255`, `design.md:L2288-L2300` | BURIED |
| D30 | EXTENDED | Tomcat `conf/server.xml`, including connector and `RemoteIpValve` configuration | `design.md:L3046-L3053`, `design.md:L3065-L3073` | BURIED |
| D31 | EXTENDED | Nginx or Apache reverse-proxy configuration | `design.md:L3094-L3112`, `design.md:L3183-L3222` | STATED PLAINLY |
| D32 | EXTENDED | Reverse-proxy access logs, including Apache tunnel-request logs / `/var/log/apache2/guac.log` | `design.md:L3274-L3281` | BURIED |
| D33 | EXTENDED | `guacamole.war` web-application deployment archive | `design.md:L1837-L1839`, `design.md:L3128-L3131` | BURIED |
| D34 | EXTENDED | Database schema and upgrade SQL scripts | `design.md:L1841-L1843`, `design.md:L1951-L1953`, `design.md:L2065-L2075` | BURIED |

## Data flows

| ID | Tier | From | To | What flows / protocol | Crosses a trust boundary? | Where it appears in design.md | Stated plainly or buried? |
|----|------|------|----|-----------------------|---------------------------|-------------------------------|---------------------------|
| F1 | EXTENDED | End user | Web browser | Keyboard, mouse, touch, clipboard, credentials, file actions | Yes — human/client boundary | `design.md:L17`, `design.md:L45` | STATED PLAINLY |
| F2 | EXTENDED | Web server / servlet container | Web browser | HTML/JavaScript Guacamole client and interface assets | Yes — server-to-client boundary | `design.md:L17` | STATED PLAINLY |
| F3 | CORE | Browser Guacamole client | Guacamole web application | Guacamole protocol over HTTP | Yes — client/server network boundary | `design.md:L17`, `design.md:L27` | STATED PLAINLY |
| F4 | EXTENDED | Guacamole web application | Browser Guacamole client | Remote display updates, audio, tunnel responses, prompts, downloads | Yes — client/server network boundary | `design.md:L27`, `design.md:L67`, `design.md:L801` | STATED PLAINLY |
| F5 | CORE | Browser Guacamole client | WebSocket tunnel endpoint | Long-lived WebSocket Guacamole tunnel | Yes — client/server network boundary | `design.md:L67`, `design.md:L3206-L3224` | BURIED |
| F6 | CORE | Browser Guacamole client | HTTP fallback tunnel endpoint | Continuous Guacamole data split across multiple short-lived HTTP streams when WebSocket is unavailable | Yes — client/server network boundary | `design.md:L67`, `design.md:L3179`, `design.md:L3274-L3276` | BURIED |
| F7 | EXTENDED | Browser / user | Web-application authentication layer | Username, password, authentication requests, session token state | Yes — authentication boundary | `design.md:L47`, `design.md:L138-L139`, `design.md:L253-L263` | STATED PLAINLY |
| F8 | EXTENDED | Guacamole web application | `guacd` | Guacamole protocol and connection instructions over TCP, normally port 4822 | Yes — separate process/network boundary | `design.md:L19`, `design.md:L35-L37`, `design.md:L184-L188` | STATED PLAINLY |
| F9 | CORE | Guacamole web application | `guacd` | Same hop as F8, **unencrypted by default** unless `guacd-ssl` and daemon TLS are configured | Yes — plaintext internal hop by default | `design.md:L190-L193`, `design.md:L1769-L1775` | BURIED |
| F10 | EXTENDED | `guacd` | Client plugin | Dynamically loaded protocol support and connection arguments | Yes — native extension/execution boundary | `design.md:L35-L37` | BURIED |
| F11 | CORE | Loaded client plugin | Guacamole web application | Plugin-controlled Guacamole-protocol communication after load; plugin operates independently of `guacd` | Yes — independently executing plugin boundary | `design.md:L37` | BURIED |
| F12 | CORE | Client plugin | Generic remote desktop server | VNC, RDP, SSH, Telnet, Kubernetes, or other protocol connection | Yes — Guacamole-to-target network boundary | `design.md:L19`, `design.md:L35`, `design.md:L75` | STATED PLAINLY |
| F13 | EXTENDED | VNC client plugin | VNC server | Outbound VNC connection, usually TCP 5900 plus display number | Yes | `design.md:L356-L364` | STATED PLAINLY |
| F14 | EXTENDED | VNC server | `guacd` / VNC client plugin | Reverse-mode inbound VNC connection to a listening `guacd` port | Yes — inbound target-to-gateway connection | `design.md:L421-L429` | BURIED |
| F15 | EXTENDED | VNC client plugin / `guacd` | PulseAudio server | Secondary unauthenticated TCP audio connection, default port 4713 | Yes — separate service/network boundary | `design.md:L433-L459` | BURIED |
| F16 | EXTENDED | RDP client plugin | RDP server | Encrypted RDP connection, normally TCP 3389 or VMConnect 2179 | Yes | `design.md:L563-L577` | STATED PLAINLY |
| F17 | EXTENDED | RDP client plugin | Remote Desktop Gateway | Gateway credentials and RDP traffic through an intermediary, normally port 443 | Yes — gateway boundary | `design.md:L901-L918` | BURIED |
| F18 | EXTENDED | RDP client plugin / initial RDP server | RDP connection broker / selected backend | Load-balance cookie or routing information and redirected connection | Yes — broker/backend boundary | `design.md:L922-L929` | BURIED |
| F19 | EXTENDED | SSH client plugin | SSH server | SSH terminal, command, environment variables, authentication, and keepalives, normally port 22 | Yes | `design.md:L1037-L1104` | STATED PLAINLY |
| F20 | EXTENDED | Browser user | SSH/SFTP server | Bidirectional file uploads and downloads over SFTP | Yes — browser through gateway to remote filesystem | `design.md:L1108-L1126`, `design.md:L1331-L1382` | BURIED |
| F21 | EXTENDED | Telnet client plugin / `guacd` | Telnet server | Telnet terminal and credentials, normally port 23; unencrypted | Yes — plaintext remote-protocol boundary | `design.md:L1172-L1200`, `design.md:L1228` | STATED PLAINLY |
| F22 | EXTENDED | Kubernetes client plugin | Kubernetes API server / container | Attach or exec terminal input/output; SSL/TLS is optional and off by default | Yes — cluster API boundary | `design.md:L1256-L1299` | STATED PLAINLY |
| F23 | EXTENDED | Browser clipboard | Remote desktop clipboard | Bidirectional clipboard data; enabled by default | Yes — user endpoint to remote endpoint | `design.md:L1319-L1327` | BURIED |
| F24 | EXTENDED | Browser | RDP virtual drive on Guacamole server and remote RDP session | File upload/download through redirected persistent drive | Yes — browser/server/remote filesystem boundaries | `design.md:L797-L803`, `design.md:L828-L849` | BURIED |
| F25 | EXTENDED | Remote RDP application | GhostScript / Guacamole client / browser | Print job converted to PDF and delivered to the browser | Yes — remote content to local client | `design.md:L801`, `design.md:L818-L821` | BURIED |
| F26 | EXTENDED | Remote RDP application | Browser JavaScript, and reverse direction | Named static RDP channels exposed as Guacamole pipes | Yes — remote application-to-browser code boundary | `design.md:L863-L866` | BURIED |
| F27 | EXTENDED | Browser JavaScript | SSH/Telnet/Kubernetes terminal session | Raw `STDIN` pipe stream, bypassing keystroke translation | Yes — browser code to remote shell/container boundary | `design.md:L1486-L1504` | BURIED |
| F28 | EXTENDED | `guacd` / protocol plugin | Broadcast or multicast network / remote host | Wake-on-LAN magic packet, default UDP port 9 | Yes — broadcast/multicast network boundary | `design.md:L1565-L1586` | BURIED |
| F29 | EXTENDED | Authentication context / token engine | Remote connection parameters and remote server | Guacamole username/password, client address/hostname, CAS attributes, and LDAP attributes substituted into connection parameters | Yes — identity data forwarded to a second system | `design.md:L1590-L1614`, `design.md:L1634-L1650` | BURIED |
| F30 | EXTENDED | `guacd` | Browser client / user, then back to connection | Prompt instruction for missing RDP/VNC authentication parameters and user-supplied response | Yes — remote-auth prompt crossing client/server boundary | `design.md:L1666-L1676` | BURIED |
| F31 | EXTENDED | Guacamole web application | `GUACAMOLE_HOME`, `guacamole.properties`, extension JARs, and libraries | Configuration and extension loading at startup/runtime | Yes — application-to-local-secret/configuration boundary | `design.md:L98-L110`, `design.md:L126-L136` | STATED PLAINLY |
| F32 | EXTENDED | Default authentication provider | `user-mapping.xml` | Read users, passwords, connection definitions, and connection credentials; automatically reread after changes | Yes — authentication process-to-credential-store boundary | `design.md:L255-L263`, `design.md:L308-L322` | BURIED |
| F33 | EXTENDED | Guacamole web application / Logback | Console and Tomcat log file | Application events and errors, including potentially detailed debug/trace data | Yes — application-to-log/audit boundary | `design.md:L210-L229` | BURIED |
| F34 | EXTENDED | `guacd` | Syslog / console | Daemon log messages | Yes — daemon-to-log/audit boundary | `design.md:L1747-L1755`, `design.md:L1796-L1799` | BURIED |
| F35 | EXTENDED | Active remote session | Graphical recording directory | Guacamole protocol dump, optionally including output, mouse events, and key events | Yes — live-session-to-persistent-evidence boundary | `design.md:L1386-L1439` | BURIED |
| F36 | EXTENDED | SSH terminal session | Typescript directory | Raw terminal text and timing information | Yes — live-session-to-persistent-evidence boundary | `design.md:L1443-L1468` | BURIED |
| F37 | CORE | Guacamole web application / database authentication extension | JDBC database server | Authentication queries and CRUD for users, groups, permissions, connections, secrets, and histories | Yes — application-to-database network boundary | `design.md:L1821-L1831`, `design.md:L2106-L2182` | STATED PLAINLY |
| F38 | EXTENDED | Other authentication extension | Database authentication extension | Successful authentication result is trusted; same-named identities are associated and data is combined | Yes — federation/identity-trust boundary | `design.md:L1823`, `design.md:L2482-L2508` | BURIED |
| F39 | EXTENDED | JDBC driver / web application | MySQL or PostgreSQL database server | Database connection that may fall back to plaintext under default `preferred` / `prefer` SSL modes | Yes — potentially plaintext database boundary | `design.md:L2225-L2243`, `design.md:L2267-L2286` | BURIED |
| F40 | EXTENDED | External browser client | Reverse proxy | HTTP/HTTPS and WebSocket requests on the public edge | Yes — Internet/edge boundary | `design.md:L3030-L3032`, `design.md:L3094-L3112` | STATED PLAINLY |
| F41 | EXTENDED | Reverse proxy | Servlet container / Guacamole web application | Proxied HTTP/WebSocket traffic, typically to port 8080 | Yes — edge-to-application boundary | `design.md:L3036-L3053`, `design.md:L3100-L3112`, `design.md:L3183-L3194` | STATED PLAINLY |
| F42 | EXTENDED | Reverse proxy | Tomcat `RemoteIpValve` / web application | `X-Forwarded-For`, `X-Forwarded-By`, and `X-Forwarded-Proto` identity/protocol headers | Yes — trusted-header boundary vulnerable to spoofing if misconfigured | `design.md:L3057-L3084` | BURIED |
| F43 | EXTENDED | Browser | Guacamole web application through Nginx | File uploads subject to proxy body-size limits | Yes — client/edge/application boundary | `design.md:L3158-L3171` | BURIED |
| F44 | EXTENDED | HTTP fallback tunnel | Apache access log | One log entry per short-lived tunnel request unless explicitly disabled | Yes — traffic-to-audit-store boundary | `design.md:L3274-L3281` | BURIED |
| F45 | EXTENDED | SSH/SFTP client plugin | `ssh_known_hosts` or per-connection host key | Host-identity lookup and verification before connection; absent file/parameter means no verification | Yes — trust-anchor boundary | `design.md:L1027-L1050` | BURIED |
| F46 | EXTENDED | `guacd` | `guacd.conf`, certificate, private key, PID file | Daemon configuration, listener binding, TLS material, and process-state output | Yes — privileged daemon-to-local-files boundary | `design.md:L1682-L1708`, `design.md:L1747-L1775` | STATED PLAINLY |
| F47 | EXTENDED | Guacamole web application | Extension JAR and JDBC-driver directories | Dynamic loading of authentication code and database drivers | Yes — code-loading/supply-chain boundary | `design.md:L106-L110`, `design.md:L1841-L1843`, `design.md:L2088-L2096` | BURIED |
| F48 | EXTENDED | Login and connection lifecycle | JDBC history tables | Login/logout and connection start/end audit records | Yes — operational-event-to-audit-store boundary | `design.md:L2698-L2720`, `design.md:L2824-L2855` | BURIED |
| F49 | EXTENDED | Administrator / administration UI or SQL client | JDBC database | Create, read, update, and delete users, groups, connections, parameters, permissions, and histories | Yes — privileged administration boundary | `design.md:L1821`, `design.md:L2544-L2548`, `design.md:L2922-L3023` | STATED PLAINLY |

## Trust boundaries

| ID | Tier | Boundary | Where it appears in design.md | Stated plainly or buried? |
|----|------|----------|-------------------------------|---------------------------|
| B1 | CORE | End user and browser versus the Guacamole deployment | `design.md:L17`, `design.md:L45` | STATED PLAINLY |
| B2 | CORE | Public client network versus reverse proxy / TLS termination edge | `design.md:L3030-L3032`, `design.md:L3094-L3112` | STATED PLAINLY |
| B3 | EXTENDED | Reverse proxy versus reduced-privilege servlet container on port 8080 | `design.md:L3032-L3038`, `design.md:L3100-L3112` | STATED PLAINLY |
| B4 | EXTENDED | Trusted reverse-proxy identity headers versus Tomcat/web-application interpretation of client identity | `design.md:L3057-L3084` | BURIED |
| B5 | CORE | Guacamole web application versus native `guacd` daemon over TCP/4822; plaintext by default | `design.md:L19`, `design.md:L37`, `design.md:L184-L193` | BURIED |
| B6 | CORE | `guacd` versus dynamically loaded client plugins that execute independently and control communication | `design.md:L35-L39` | BURIED |
| B7 | CORE | Guacamole server / client plugins versus remote VNC, RDP, SSH, Telnet, Kubernetes, SFTP, gateway, broker, and PulseAudio systems | `design.md:L19`, `design.md:L358-L364`, `design.md:L565-L577`, `design.md:L1039-L1048`, `design.md:L1174-L1180`, `design.md:L1258-L1299` | STATED PLAINLY |
| B8 | CORE | Guacamole web application and authentication extensions versus external database server | `design.md:L1821-L1831`, `design.md:L2106-L2182` | STATED PLAINLY |
| B9 | EXTENDED | Guacamole authentication framework versus external/federated identity providers and their asserted attributes/results | `design.md:L1823`, `design.md:L1634-L1650` | BURIED |
| B10 | CORE | Guacamole processes versus local filesystem stores containing configuration, credentials, keys, extensions, transferred files, and recordings | `design.md:L98-L110`, `design.md:L261-L263`, `design.md:L848-L850`, `design.md:L1388-L1468`, `design.md:L1682-L1708` | BURIED |
| B11 | EXTENDED | Browser-supplied clipboard, file, pipe, and authentication data versus remote desktops, shells, and containers | `design.md:L803`, `design.md:L863-L866`, `design.md:L1108-L1124`, `design.md:L1319-L1327`, `design.md:L1486-L1504` | BURIED |
| B12 | EXTENDED | Broadcast/multicast network boundary used by Wake-on-LAN | `design.md:L1565-L1586` | BURIED |

## Notes

1. **System boundary is not declared explicitly.** The inventory treats the Guacamole deployment as the web application, servlet container, `guacd`, its plugins/libraries, and optional reverse proxy. Remote targets, identity providers, databases, browsers, and network infrastructure are treated as external or boundary-adjacent.
2. **The critical hidden finding is recorded separately.** `guacd-ssl` states that communication from the web application to `guacd` is unencrypted by default at `design.md:L190-L193`. The same choice can be overridden per database-backed connection through `proxy_encryption_method` at `design.md:L2786-L2787`.
3. **`guacd` port 4822 is explicit but easy to miss.** It appears in the web-application property table at `design.md:L187-L188`, in `guacd.conf` at `design.md:L1695-L1698`, and in the daemon listener description at `design.md:L1761-L1765`.
4. **`libguac` is not a process.** It is retained in the Processes section because it is an architecture-significant runtime component shared by `guacd` and every plugin. A strict DFD could instead record it only in Notes.
5. **Client-plugin isolation is underspecified.** The document says a loaded plugin “runs independently of `guacd`” and controls communication until termination (`design.md:L37`), but it does not say whether this means a child process, thread, library callback, or another isolation mechanism.
6. **Browser and user are separate rows for threat-model granularity.** A coarser DFD may merge them into one external actor.
7. **Generic and protocol-specific remote servers are both retained.** The generic remote desktop server is the architecture-level entity; VNC, RDP, SSH, Telnet, Kubernetes, SFTP, gateways, and brokers are distinct concrete endpoints with materially different security properties.
8. **Optional components remain ground-truth elements.** Reverse proxies, database authentication, RDP gateways/brokers, PulseAudio, recordings, file transfer, and Wake-on-LAN are configuration-dependent, but the document presents them as supported architecture and data paths.
9. **Historical components are not scored as current architecture.** RealMint, its PHP long-poll tunnel, the proof-of-concept XML VNC client, and SourceForge are historical narrative at `design.md:L51-L67`. They are not included as current elements.
10. **Vendor examples are grouped rather than individually scored.** RealVNC, TigerVNC, TightVNC, x11vnc, vino, QEMU/KVM, individual JDBC vendors, and similar product examples are implementation choices for already-listed entities, not separate mandatory architecture elements.
11. **OpenID, SAML, and TOTP are weakly specified here.** OpenID and SAML appear mainly in an extension-load example (`design.md:L177-L180`); TOTP appears in the account auto-creation discussion (`design.md:L2506`). CAS and LDAP have explicit server-to-token flows and are therefore listed; the others should not be scored as required standalone flows.
12. **Database tables are grouped by security-relevant logical store.** The document names individual tables. Closely related tables are grouped where separating them would not change the threat model, while password history, audit histories, connection parameters, sharing profiles, groups, and permissions remain separate because their contents and risks differ.
13. **Connection parameters may contain secrets.** The document describes arbitrary parameter values (`design.md:L2799-L2808`) and elsewhere defines password, private-key, passphrase, gateway-password, SFTP password/key, client certificates, and other sensitive parameters. A model need not enumerate every parameter name to receive credit for identifying the connection-secret store.
14. **Protocol security differs by path.** RDP is stated to be encrypted (`design.md:L577`); Telnet is unencrypted (`design.md:L1148`, `design.md:L1228`); Kubernetes TLS is off by default (`design.md:L1284-L1288`); SSH host verification is off unless a trust anchor is supplied (`design.md:L1029-L1033`); JDBC defaults may allow plaintext fallback (`design.md:L2233-L2235`, `design.md:L2276-L2277`).
15. **Trust-boundary markings are partly inferential.** The document describes processes, hosts, ports, privilege levels, and network crossings but does not draw explicit boundary lines. “Crosses a trust boundary” is marked where data moves between independently controlled processes, hosts, privilege domains, identity authorities, or persistent secret/audit stores.
16. **Plain versus buried is qualitative, not a word-count rule.** Deeply nested configuration rows and narrative asides are marked `BURIED` even where the item has a heading or appears more than once.
17. **No prompt variants were used to construct this inventory.** Only the supplied `design.md` and blank `elements.md` template were opened.
18. **Methodological provenance.** The initial inventory was authored by ChatGPT, an out-of-family model relative to the model family intended for testing. It must not be described as hand-built. The defensible description is: “ground truth built by an out-of-family model, then reviewed and signed off line by line by a human.” The human reviewer completed the end-to-end inventory review and signed off the exact Tier column on 2026-07-12 before any scored run.
19. **Tiering controls the floor effect.** CORE uses canonical architectural units and deliberately avoids scoring every protocol-specific instance as mandatory. EXTENDED preserves the maximal inventory without allowing peripheral detail or DFD granularity to dominate the headline metric.
20. **Granularity rule.** A model receives CORE credit for a semantically equivalent grouped element. For example, “remote desktop targets (VNC/RDP/SSH/Telnet/Kubernetes)” satisfies the canonical remote-target row; it is not required to enumerate each EXTENDED protocol-specific entity. This grouped-credit allowance applies to entity and component granularity only. It does not allow a generic architecture statement to satisfy a distinct security-property row.
21. **Security-property credit rule.** F9 and B5 require the security property, not merely the existence of the hop. Credit is earned only if the output states that the web-application-to-`guacd` connection is unencrypted or plaintext by default, or identifies a threat that necessarily depends on that fact, such as interception, tampering, or credential capture on the internal hop. Describing the connection, naming TCP/4822, or listing `guacd` as a component does not earn F9 or B5. The same principle applies to other default-off or fallback security properties, including Kubernetes TLS being disabled by default, SSH host verification being absent unless a trust anchor is configured, and JDBC modes that may fall back to plaintext. Security properties must be stated or used explicitly in threat reasoning; they are not inferred from generic component or flow coverage.
22. **Truncation control.** CORE and EXTENDED must be scored independently, and output limits must be held constant across arms. Failure to enumerate EXTENDED rows must not be interpreted as silent CORE coverage loss.
23. **Pre-registration rule.** The human reviewer signed off the exact Tier column before any model run. The 31-row CORE set and scoring rules are frozen under Git tag `yardstick-v1.0.0`. Any correction after a run must create a new version, identify the changed rows, and rerun all arms rather than editing the active yardstick around observed outputs.

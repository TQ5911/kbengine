#!/bin/bash
ps -ef |grep -v grep | grep -E 'centralLogin|admin|auction|router|maple|dropServer|leaseServer|crossDataServer|queueServer|orderService|allianceService'

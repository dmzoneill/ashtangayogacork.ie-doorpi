#!/bin/bash 

export RECIPIENT="dmz.oneill@gmail.com"
export FROM="suicidalbeanbag@gmail.com"
export FROMNAME="Rick James"
export TIME=$(date)

OUTFILE="/tmp/mail"
SMTPHOST="smtps://smtp.gmail.com:465"
APPPW=$(cat /var/lib/motion/.google-app-password)
echo $APPPW

cat >$OUTFILE <<EOL
From: "$FROMNAME" <$FROM>
To: $RECIPIENT
Subject: AYC - Movement $TIME

movement $TIME

EOL

#curl --ssl --url "$SMTPHOST" --ssl-reqd --mail-from "$FROM" --mail-rcpt "$RECIPIENT" -T "$OUTFILE" -u "$FROM:$APPPW" --anyauth

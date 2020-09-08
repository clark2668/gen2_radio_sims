# gen2_radio_sims
repository for gen2 radio sims stuff

## to submit jobs, need to do
grid-proxy-init -hours 72

export X509_USER_PROXY=/tmp/x509up_u$UID

## git maintenance
if you are keeping the repo on sub-1, which has an oudated version of git, you will also need to do:

`git remote set-url origin https://clark2668@github.com/clark2668/grid_scripts.git`

or else pushing won't work
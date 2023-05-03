cd /usr/bin/ || exit

unzip fastqc_v0.11.9.zip
rm fastqc_v0.11.9.zip
chmod a+x /usr/bin/FastQC/fastqc

cd - || return
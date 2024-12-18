
# PassmaoPWNR-Ineitor

`PassmaoPWNR-Ineitor` is a tool we made to test how fast we could crack `NTLM` hashes using precomputed wordlists.

It makes use of `blosc` to divide the wordlists and it uses indexes to reduce to the minimum the amount of blocs needed to complete a hash search.

![image](https://github.com/user-attachments/assets/31e383c2-b2e6-4a35-bf4b-f0e3c45a2b38)


Made in Spanish and English, and it only requires to install `blosc`, every other package is native from python



## Quick usage
```
usage: PassmaoPWNR-Ineitor.py [-h] [-f FILEHASHESH] [-H HASH] [-p PATHBLOCS] [-of OUPUTFILE] [-T BLOCTYPE] [-b BRUTEFILE] [-s BLOCSIZE] [-t THREADS] action

Gestor de acciones

positional arguments:
  action                Selected action / Acción a realizar: search, generateBlocs, sort

options:
  -h, --help            show this help message and exit
  -f FILEHASHESH, --filehashesh FILEHASHESH
                        File with the hashes / Archivo con hashesh para crackear
  -H HASH, --hash HASH  
                        Individual hash / Hash individual a encontrar
  -p PATHBLOCS, --pathblocs PATHBLOCS
                        Path to the blocs file directory / Ruta a archivos Blocs
  -of OUPUTFILE, --ouputfile OUPUTFILE
                        File to output the found hashes / Ruta archivo output
  -T BLOCTYPE, --bloctype BLOCTYPE
                        Blocks format is .blosc or .txt / Se ha comprimido en formato TXT o Blosc. 
                        Default: blosc
  -b BRUTEFILE, --brutefile BRUTEFILE
                        File with the precalculated hashes / Archivo con hashesh precalculados
  -s BLOCSIZE, --blocsize BLOCSIZE
                        Size of each block in bytes / Tamaño de cada bloque en bytes. 
                        Default: 100000000
  -t THREADS, --threads THREADS
                        Simultaneous threads used / Cantidad de procesos simultaneos. 
                        Default: 1

```
### Single hash
```
python PassmaoPWNR-Ineitor.py search -H c46b9e588fa0d112de6f59fd6d58eae3 -p C:\Wordlists\Blocs -of C:\Results\result.txt
```

### Hashfiles
```
python PassmaoPWNR-Ineitor.py search -f C:\Hashfiles\hashfile.txt -p C:\Wordlists\Blocs -of C:\Results\result.txt
```

### TXT Wordlist
```
python PassmaoPWNR-Ineitor.py search -f C:\Hashfiles\hashfile.txt -p C:\Wordlists\Blocs -T txt -of C:\Results\result.txt
```

### Multiple threads
```
python PassmaoPWNR-Ineitor.py search -f C:\Hashfiles\hashfile.txt -p C:\Wordlists\Blocs -of C:\Results\result.txt -t 10
```

### Create blocs
```
python PassmaoPWNR-Ineitor.py generateBlocs -b C:\Wordlists\PrecomputedNTLM-1.txt -p C:\Wordlists\Blocs
```

### Change blocs size (Example with 50MB)
```
python PassmaoPWNR-Ineitor.py generateBlocs -b C:\Wordlists\PrecomputedNTLM-1.txt -p C:\Wordlists\Blocs -s 50000000
```

### Create TXT blocs
```
python PassmaoPWNR-Ineitor.py generateBlocs -b C:\Wordlists\PrecomputedNTLM-1.txt -p C:\Wordlists\Blocs -T txt
```

### Sort a Wordlist
```
python PassmaoPWNR-Ineitor.py sort -b C:\Wordlist\PrecomputedNTLM-1.txt
```
## Usage example

For the use of this tool is undispensable to have a precomputed wordlist. We took ours from [weakpass](https://weakpass.com/pre-computed).

First of all you want to download the zip form Github and decomrpess on a directory of your liking.
Once decomrpessed, the requirements should be installed by making use of the following command:

```
pip install -r requirements.txt 
```

Once the requirements are installed its time to take care of the wordlist. The first thing to do with it is to decomrpess it. And once decomrpessed is possible to start creating the blocs based on the wordlist.

```
python PassmaoPWNR-Ineitor.py createBlocs -b [Path to wordlist] -p [Bloc oputput path] -s [Block size (Default 100000000)]
```

The blocs take a lot of time to create, so be patient
After the creation of the blocs its time for the last step, the comparation of the NTLM hashes against the blocs

```
python PassmaoPWNR-Ineitor.py search -f [file with the NTLM hashes] -p [path with the bloc files] -of [Output file] -t [cuantity of threads used]
```

With that at least a couple hundred of NTLM hashes shoud be stored with their cleartext password into the output file
## License

Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
## Authors

- Naresh Zubiarrain `N7r3te`, you can contact me by  `Github` ([N7r3te](https://github.com/Narete)), `twitter` ([@Narete_](https://x.com/Narete_)) or by [Linkedin](https://www.linkedin.com/in/naresh-zubiarrain-torreño-a62070239/)
- Dimas Pastor `pip0x`, you can contact me by `Github` ([pip0x](https://github.com/pip0x/)) or by [Linkedin](https://www.linkedin.com/in/dimas-pastor/)

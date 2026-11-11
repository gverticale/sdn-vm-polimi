# Laboratorio per corso di Software Defined Networking @ Politecnico di Milano
Questo laboratorio puo' essere svolto in due modi diversi:
1. Utilizzando le [VM fornite](#1-svolgimento-con-le-vm-fornite) (**Consigliato**)
2. Utilizzando [Docker](#2-svolgimento-con-docker)

## 1. Svolgimento con le VM fornite
Sono state fornite delle macchine virtuali con tutti i pacchetti necessari per svolgere il laboratorio. Queste macchine virtuali sono state create per funzionare sia con architetture x86_64 che con architetture ARM64. 

Per avviare le macchine virtuali, è necessario utilizzare un provider di virtualizzazione (es. Virtualbox o VMware) e seguire le istruzioni fornite insieme alle macchine virtuali.

### Windows, Linux o MacOS with Intel/AMD CPU
1. Installare [Virtualbox](https://www.virtualbox.org)
2. Scaricare la macchina virtuale dal [questo](https://polimi365-my.sharepoint.com/:u:/g/personal/10524482_polimi_it/IQA_O2XzjsN9S5JOAS-nG2LcAUlboUspxLJKb3glyDErICI?e=X7aCPM) link.
    - Il link è accessibile solo agli studenti del Politecnico di Milano, previa autenticazione con le credenziali istituzionali.
    - Se si vuole verificare che il file scaricato sia corretto, verificando l'hash direttamente cosi:
        ```bash
        $ echo "f95c015797924a18600116a1e49ae11b602c5abdb991fefefe3992262b4c350a  sdn-labs-amd64.ova" | sha256sum -c -
        ```
      Il confronto darà esito positivo se l'output riporta OK, altrimenti ritorna FAILED.
3. Aprire il file `.ova` con Virtualbox e seguire le istruzioni per importare la macchina virtuale.
4. Avviare la macchina virtuale e attendere che sia completamente avviata.
5. Le credenziali di accesso sono:
    - Username: `sdn`
    - Password: `sdn`
6. Una volta dentro la VM, aprire il terminale e clonare il repository con il comando:
    ```bash
    $ git clone https://github.com/gverticale/sdn-vm-polimi.git
    ```
    - Nel caso in cui la cartella sia gia' presente, e' possibile aggiornarla con il comando:
        ```bash
        $ cd sdn-vm-polimi
        $ git pull
        ```
7. Entrare nella cartella ed avviare il docker con il comando:
    ```bash
    $ cd sdn-vm-polimi
    $ make connect-docker
    ```

### MacOS with Apple Silicon (ARM64)
1. Installare [VMware Fusion](https://www.vmware.com/products/fusion.html)
    - È necessario avere un account VMWare Customer Connect per procedere al download. È possibile iscriversi mediante l'indirizzo email del Politecnico o tramite quello personale: la licenza per VMWare Fusion Player è gratuita sia per scopi personali che per gli studenti.
2. Scaricare la macchina virtuale dal [questo](https://polimi365-my.sharepoint.com/:u:/g/personal/10457521_polimi_it/EcFxgKNEHa9PoCUc_k7CUtwBCqA1ixcDVzptJFa2B0KB-g?e=A3W43Q) link.
    - Il link è accessibile solo agli studenti del Politecnico di Milano, previa autenticazione con le credenziali istituzionali.
3. Estrarre il file `sdn-labs-arm634.vmwarevm` dall'archivio `.zip` e posizionarlo in una cartella a piacere.
4. Aprire VMware Fusion e selezionare `File` -> `Apri...` e selezionare il file `sdn-labs-arm634.vmwarevm`.
5. Quando la macchina virtuale si avvia, verrà chiesto se la macchina virtuale è stata spostata o copiata. Selezionare `Copiata`.
6. Attendere che sia completamente avviata.
5. Le credenziali di accesso sono:
    - Username: `sdn`
    - Password: `sdn`
6. Una volta dentro la VM, aprire il terminale e clonare il repository con il comando:
    ```bash
    $ git clone https://github.com/gverticale/sdn-vm-polimi.git
    ```
    - Nel caso in cui la cartella sia gia' presente, e' possibile aggiornarla con il comando:
        ```bash
        $ cd sdn-vm-polimi
        $ git pull
        ```
7. Entrare nella cartella ed avviare il docker con il comando:
    ```bash
    $ cd sdn-vm-polimi
    $ make connect-docker
    ```

## 2. Svolgimento con Docker
Docker è una piattaforma per lo sviluppo, la distribuzione e l'esecuzione di applicazioni in container. In questo caso, verrà utilizzato per creare un container con un sistema operativo Ubuntu 20.04 LTS, con tutti i pacchetti necessari per svolgere il laboratorio.
Anche in questo caso, in base al sistema operativo dell'host ed all'architettura del processore, e' necessario eseguire delle istruzioni diverse.

### Windows
Il supporto a Docker su Windows è limitato. È possibile installare Docker Desktop, ma non è garantito che funzioni correttamente dato che Windows Subsystem for Linux (WSL2) è limitato nel numero di interfacce e moduli kernel. È fortemente consigliato l'utilizzo della macchina virtuale fornita.

### Linux
1. Installare Docker:
    ```bash
    # Add Docker's official GPG key:
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    ```

    ```bash
    # Install Docker
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```
2. Nel caso in cui si voglia utilizzare Docker senza `sudo`, aggiungere l'utente al gruppo `docker`:
    ```bash
    sudo usermod -aG docker $USER
    newgrp docker
    ```

### MacOS
1. Installare Docker dal [sito web](https://www.docker.com/get-started/).

### Istruzioni post installazione
1. Una volta installato il Docker Engine, verificare che questo funzioni correttamente eseguendo il comando:
    ```bash
    sudo docker run hello-world
    ```
2. Entrare nella cartella del laboratorio.
3. Avviare il container con il comando:
    ```bash
    make connect-docker
    ```
    - La prima volta che viene eseguito, questo comando proverà a scaricare l'immagine del Docker per il laboratorio. Questo potrebbe richiedere del tempo.
    - Una volta avviato, si aprirà una nuova shell all'interno del container e sara' possibile svolgere il laboratorio.
4. Per aprire altre shell all'interno del container, eseguire, su un altro terminale, il comando:
    ```bash
    make connect-docker
    ```

## Problemi generici

### Linux

#### Docker deamon non attivo

È opportuno controllare se il demone è veramente disattivato:
```bash
systemctl status docker --no-pager
```
Se confermato, riattivarlo in questo modo:
```bash
sudo systemctl start docker
sudo systemctl enable docker
```
e riprovare a lanciare il container.

#### Installazione di Virtualbox per poi scaricare la virtual machine
Il metodo più raccomandato è quello di installare Virtualbox direttamente dalla repository ufficiale:
```bash
# aggiornare il sistema
sudo apt update
sudo apt upgrade -y
# installare il pacchetto specifico gnupg2
sudo apt install wget gnupg2 -y
# aggiungere la chiave GPG ufficiale di oracle
wget -O- https://www.virtualbox.org/download/oracle_vbox_2016.asc | \
sudo gpg --dearmor -o /usr/share/keyrings/virtualbox.gpg
# aggiungere al repository apt il repository di virtualbox
echo "deb [signed-by=/usr/share/keyrings/virtualbox.gpg] https://download.virtualbox.org/virtualbox/debian jammy contrib" | \
sudo tee /etc/apt/sources.list.d/virtualbox.list
# aggiornare il sistema di nuovo
sudo apt update
# installare virtualbox
sudo apt install virtualbox-7.0 -y
```

Se si dovesse incorrere in qualche problematica, uno dei problemi è potrebbe essere legato all'attivazione del secure boot. Altrimenti all'interno del file di log ```/var/log/vbox-setup.log``` è possibile controllare quale sia l'errore nello specifico.

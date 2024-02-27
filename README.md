# Laboratorio per corso di Software Defined Networking @ Politecnico di Milano
Questo laboratorio puo' essere svolto in due modi diversi:
1. Utilizzando [Vagrant](#1-svolgimento-con-vagrant) ed un sistema di virtualizzazione (es. Virtualbox o VMware) (**Consigliato**)
2. Utilizzando [Docker](#2-svolgimento-con-docker)

## 1. Svolgimento con Vagrant
Vagrant è uno strumento per la creazione e la gestione di macchine virtuali. In questo caso, verrà utilizzato per creare una macchina virtuale con un sistema operativo Ubuntu 20.04 LTS, con tutti i pacchetti necessari per svolgere il laboratorio.
In base al sistema operativo dell'host ed all'architettura del processore, e' necessario eseguire delle istruzioni diverse.

#### Windows
1. Installare [Virtualbox](https://www.virtualbox.org)
2. Installare [Vagrant per Windows](https://developer.hashicorp.com/vagrant/install?product_intent=vagrant#windows)

#### Linux
1. Installare [Virtualbox](https://www.virtualbox.org)
2. Installare [Vagrant per Linux](https://developer.hashicorp.com/vagrant/install?product_intent=vagrant#linux)
    ```bash
    $ wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
    $ echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
    $ sudo apt update && sudo apt install vagrant
    ```

#### MacOS
1. Installare [VMware Fusion](https://www.vmware.com/products/fusion.html)
    - È necessario avere un account VMWare Customer Connect per procedere al download. È possibile iscriversi mediante l'indirizzo email del Politecnico o tramite quello personale: la licenza per VMWare Fusion Player è gratuita sia per scopi personali che per gli studenti.
2. Installare [Vagrant per MacOS](https://developer.hashicorp.com/vagrant/install?product_intent=vagrant#macos)
    ```bash
    $ brew tap hashicorp/tap
    $ brew install hashicorp/tap/hashicorp-vagrant
    ```

### Istruzioni
1. Aprire il provider di virtualizzazione (es. Virtualbox o VMware) e verificare che sia installato correttamente. Tenere la finestra aperta mentre vengono eseguiti gli altri comandi.
2. Copiare i file di configurazione in una cartella vuota. Se si vuole si può usare git.
    - Nel caso di git, il comando da eseguire e' il seguente:
        ```bash
        $ git clone https://github.com/gverticale/sdn-vm-polimi.git
        ```
3. Aprire una finestra del teminale in questa nuova cartella.
4. Istanziare e avviare la macchina con `vagrant up`
    - Una volta avviata, si aprira' una nuova finestra del provider di virtualizzazione, che mostrera' la macchina virtuale in esecuzione.
    - Attendere fino a quando la macchina virtuale non e' completamente avviata e tutti i pacchetti non sono stati installati.
5. E' possibile utilizzare direttamente la macchina virtuale tramite il provider di virtualizzazione, oppure collegarsi ad essa tramite `vagrant ssh`
    - La macchina virtuale e' gia' configurata con un utente `vagrant` con password `vagrant`
6. Il disco della macchina host è montato nella cartella `/vagrant`
7. Per spegnere la macchina, uscire dalla macchina (`exit`) e fermarla (`vagrant halt`)
8. Per cancellare la macchina, uscire dalla macchina (`exit`) e cancellarla (`vagrant destroy`)

## 2. Svolgimento con Docker
Docker è una piattaforma per lo sviluppo, la distribuzione e l'esecuzione di applicazioni in container. In questo caso, verrà utilizzato per creare un container con un sistema operativo Ubuntu 20.04 LTS, con tutti i pacchetti necessari per svolgere il laboratorio.
Anche in questo caso, in base al sistema operativo dell'host ed all'architettura del processore, e' necessario eseguire delle istruzioni diverse.

### Windows
Il supporto a Docker su Windows è limitato. È possibile installare Docker Desktop, ma non è garantito che funzioni correttamente. Si consiglia di utilizzare Vagrant.

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

### MacOS
1. Installare Docker dal [sito web](https://www.docker.com/get-started/).

### Istruzioni
1. Una volta installato Docker Engine, verificare che questo funzioni correttamente eseguendo il comando:
    ```bash
    $ sudo docker run hello-world
    ```

2. Entrare nella cartella del laboratorio.
3. Avviare il container con il comando:
    ```bash
    $ make connect-docker
    ```
    - La prima volta che viene eseguito, questo comando proverà a scaricare l'immagine del Docker per il laboratorio. Questo potrebbe richiedere del tempo.
    - Una volta avviato, si aprirà una nuova shell all'interno del container e sara' possibile svolgere il laboratorio.
4. Per aprire altre shell all'interno del container, eseguire, su un altro terminale, il comando:
    ```bash
    $ make connect-docker
    ```

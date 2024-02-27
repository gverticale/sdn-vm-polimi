# Macchina virtuale per il corso di Software Defined Networking @ Politecnico di Milano

(work in progress)

Istruzioni per Windows, Linux e Mac con architettura amd64. Per Mac con architettura arm consultare questa pagina di istruzioni https://github.com/MrVideo/sdn-lab (courtesy of Mario Merlo)

## Requisiti:
* Virtualbox (https://www.virtualbox.org)
* Vagrant (https://www.vagrantup.com)
* Un client ssh

## Istruzioni
1. Installare virtualbox e vagrant.
2. Copiare i file di configurazione in una cartella vuota. Se si vuole si può usare git.
3. Aprire una finestra del teminale in questa nuova cartella.
4. Istanziare e avviare la macchina con `vagrant up`
5. Per collegarsi alla macchina virtuale `vagrant ssh`
6. Il disco della macchina host è montato nella cartella `/vagrant`
7. Per spegnere la macchina, uscire dalla macchina (`exit`) e fermarla (`vagrant halt`)

## Istruzioni (Apple Silicon)
1. Installare Docker dal [sito web](https://www.docker.com).
2. Installare Visual Studio Code dal [sito web](https://code.visualstudio.com).
3. Installare, su VSCode, il [plugin](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) per Docker.
4. Copiare la cartella `docker-sdn` in una cartella vuota. Se si vuole si può usare git.
5. Aprire una finestra del terminale in questa nuova cartella.
7. Eseguire
```
docker build -t sdn docker-sdn
```
8. Spostandosi nella cartella `docker-sdn` tramite il comando `cd docker-sdn`, stanziare e avviare il container con:
```
docker-compose run --rm sdn
```
9. In VSCode, dopo aver premuto l'icona nell'angolo in basso a sinistra, selezionare "Attach to Running Container", e selezionare il container con il prefisso `docker-sdn`.

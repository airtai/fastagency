## Workflow
- sync: Ag2Workflows
- async: AutogenChatWorkflows
	- agents need run methods not just declarations -> callable u konstruktoru?

## FastApiAdapter
- u konstruktoru moze primiti sync i async workflow, i prilagoditi ce se tome (potencijalno vratiti odgovarajucu vrstu objekta)
- provider kojeg dobijemo od njega ce biti sync (jer trenutno samo mesop koristi njegov provider). Ako cemo dodavati i async varijantu providera, onda ce se on dohvatiti sa .async_provider

## NATSAdapter
- u konstruktoru moze primiti sync i async workflow, i prilagoditi ce se tome
- Moze vratiti i sync i async provider. Jer za FastApiAdapter cemo prirodno koristiti async verziju providera, a u Mesopu sync.
	- .provider
	- .async_providerr

## FastAgencyApp
- trenutno neka podrzi samo sync providere, jer je to ono sto nam Mesop trosi
- ako ce se jednom pojaviti pyhton app kojem vise odgovara async, onda cemo podrzati async providere.

## SyncAdapter
- uzme async provider, i napravi sync provider
- koristi ga toplogija Mesop|Autogenchat da si adaptira async wf u sync

## Poruke
- unija postojecih i potrebnih za autogenchat
- generic message type

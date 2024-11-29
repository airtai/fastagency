## Workflow
- sync: Ag2Workflows
- async: AutogenChatWorkflows
	- agents need run methods not just declarations -> callable u konstruktoru?
	- treba mogucnost biranje wrste teama

## FastApiAdapter
- u konstruktoru moze primiti sync i async workflow, i prilagoditi ce se tome (potencijalno vratiti odgovarajucu vrstu objekta, ili mozemo imati razlicite Adapter klase)
- provider kojeg dobijemo od njega ce biti sync (jer trenutno samo mesop koristi njegov provider). Ako cemo dodavati i async varijantu providera, onda ce se on dohvatiti sa .async_provider

## NATSAdapter
- u konstruktoru moze primiti sync i async workflow, i prilagoditi ce se tome
- Moze vratiti i sync i async provider. Jer za FastApiAdapter cemo prirodno koristiti async verziju providera, a u Mesopu sync.
	- .provider
	- .async_provider

## FastAgencyApp
- trenutno neka podrzi samo sync providere, jer je to ono sto nam Mesop i console trosi
- ako ce se jednom pojaviti pyhton app kojem vise odgovara async, onda cemo podrzati async providere.

## SyncAdapter
- uzme async provider, i napravi sync provider
- koristi ga toplogija Mesop|Autogenchat da si adaptira async wf u sync

## Poruke
- unija postojecih i potrebnih za autogenchat
- generic message type

## Problemi
- ako necemo moci imati istovremeno instaliran ag2 i autogen, sto ce biti sa testovima?
- pre_commit missing in 0.4 dev container?

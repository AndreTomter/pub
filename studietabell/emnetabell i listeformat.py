import requests
from requests.auth import HTTPBasicAuth
from collections import defaultdict
import json
import pandas as pd
import re
from datetime import datetime
#må kanskje hente inn eier nivå#

# Brukernavn og passord
username = "uib_studieelementer_les1"
password = "Foiv;OvyicIjceg2"

# Funksjon for å utføre GraphQL-spørringen med autentisering
def run_query(query, username, password, variables=None):
    url = "https://api.fellesstudentsystem.no/graphql/"
    headers = {
        "Content-Type": "application/json", 
        "Feature-Flags": "beta,experimental"
        }
    auth = HTTPBasicAuth(username, password)
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers, auth=auth)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")
'''
defquery = """
{
  __schema {
    types {
      name
      kind
      fields {
        name
        type {
          name
          kind
        }
      }
    }
  }
}
"""
result = run_query(defquery, username, password)
data = result
# Filtrer etter en bestemt type
target_type = "KullTerminbetegnelse"  # Endre til den typen du leter etter

filtered_types = [
    t for t in data["data"]["__schema"]["types"]
    if t["name"] == target_type
]

# Skriv ut resultatet
if filtered_types:
    print(filtered_types[0])  # Viser detaljer om den spesifikke typen
else:
    print(f"Ingen treff for typen {target_type}")



query = """
{
  __schema {
    types {
      name
      kind
      enumValues {
        name
      }
    }
  }
}
"""

response = run_query(query, username, password)
data = response

# Filtrer ut ENUM-typer
enum_types = [t for t in data["data"]["__schema"]["types"] if t["kind"] == "ENUM"]

print(enum_types)  # Viser tilgjengelige ENUM-typer
'''


def hent_id_for_terminbetegnelse(terminbetegnelse = None):
    # Gå gjennom listen 'edges' for å finne "HØST"
    data = run_query(terminbetegnelsequery, username, password)

    for edge in data['data']['terminbetegnelser']['edges']:
        if edge['node']['kode'] == terminbetegnelse:
            return edge['node']['id']
    return None

terminbetegnelsequery = """
{
    terminbetegnelser(filter: {eierOrganisasjonskode: "184"}) {
        edges {
            node {
                id
                kode
            }
        }
    }
}
"""

terminquery = """
query MyQuery($arstall: [Int!], $terminbetegnelser: [ID!]) {
  terminer(
    filter: {eierOrganisasjonskode: "184", arstall: $arstall, terminbetegnelser: $terminbetegnelser}
  ) {
    edges {
      node {
        id
        betegnelse {
          kode
          id
        }
        arstall
      }
    }
  }
}


terminbetegnelse = hent_id_for_terminbetegnelse('VÅR')
arstall = 2018
variables = {"arstall": arstall, "terminbetegnelser": terminbetegnelse}

result = run_query(terminquery, username, password, variables)
print(result)
quit()
"""
from bs4 import BeautifulSoup
soup_nav = BeautifulSoup('''''', '''html.parser''')
tab_tag = soup_nav.new_tag("div")
tab_tag.attrs['class']='tab'
soup_nav.append(tab_tag)

def artermin(arstall, terminbetegnelse):
    termin = 0
    if terminbetegnelse[0] == 'H':
        termin = 2
    if terminbetegnelse[0] == 'V':
        termin = 1
    arterminkode = f'''{arstall}{termin}'''
    return arterminkode

#Inneværende år
innevar = datetime.now().year
innevdato = datetime.now()

# Sjekk om vi er før 1. juli
termin = 1 if innevdato.month < 7 else 2
innevartermin = f'''{innevar}{termin}'''


ar=[2024,2023,2022,2021,2020,2019,2018]
ar=[2022]
maxar = max(ar)

for arstall in ar:
  ar_tab_tag = soup_nav.new_tag("button")
  if arstall == maxar:
    ar_tab_tag.attrs['class']='tablinks active'
  if arstall != maxar:
    ar_tab_tag.attrs['class']='tablinks'
  ar_tab_tag.string=f'''{arstall}'''
  ar_tab_tag.attrs['onclick']=f'''valgtArstallKull(event, '{arstall}')'''
  find_tag_tag = soup_nav.find(class_='tab')
  find_tag_tag.append(ar_tab_tag)

  studieprogramkoder = ["BASV-GEOG"]
 


  terminbetegnelse = 'HOST'

  programkullartermin = artermin(arstall, terminbetegnelse)

  filer = []

  query = """
  query MyQuery($cursor: String, $studieprogramkode: String!, $arstall: Int!, $betegnelse: KullTerminbetegnelse!) {
    studieoppbygninger(
      filter: {eierOrganisasjonskode: "184", kull: {arstall:  $arstall, betegnelse: $betegnelse, studieprogramkode: $studieprogramkode}}, after: $cursor
    ) {
      edges {
        node {
          alleOppbygningsdeler {
            rekkefolgenummer
            studieoppbygningsdel {
              kode
              navnAlleSprak {
                nb
              }
              vektingskrav {
                minimumsvekting {
                  verdi
                }
              }
              beskrivelseAlleSprak {
                nb
              }
              veivalg {
                harVeivalg
                antallVeivalg
              }
              utdanningsplanelementer {
                utdanningsplanelement {
                  kode
                }
                terminForPlasseringIUtdanningsplan {
                  terminnummerFra
                  terminnummerTil
                }
              }
              frieEmnevalg {
                begrensninger {
                    organisasjonsenhet {
                        instituttnummer
                        fakultet {
                            fakultetsnummer
                        }
                        gruppenummer
                        navnAlleSprak {
                            nb
                        }
                    }
                    studieniva {
                        fraStudieniva {
                            kode
                        }
                        tilStudieniva {
                            kode
                        }
                    }
                    fag {
                        navnAlleSprak {
                            nb
                        }
                    }
                    emnekategori {
                        kode
                        navnAlleSprak {
                            nb
                        }
                    }
                    }
                }
              emner {
                emne {
                  kode
                  vekting {
                    emnevekting {
                      verdi
                    }
                  }
                  navnAlleSprak {
                    nb
                  }
                }
                kullterminer {
                  tilKullTermin {
                    arstall
                    betegnelse {
                      kode
                    }
                    id
                  }
                  fraKullTermin {
                    arstall
                    betegnelse {
                      kode
                    }
                    id
                  }
                }
                rekkefolgenummer
                sisteTerminForValg {
                  arstall
                  betegnelse {
                    kode
                  }
                  id
                }
                terminForPlasseringIUtdanningsplan {
                  terminnummerForhandsvalgt
                  terminnummerFra
                  terminnummerTil
                }
                valgregel {
                  kode
                  navnAlleSprak {
                    nb
                  }
                  erObligatorisk
                }
              }
            }
            kullterminer {
              kullStartFraTermin {
                id
                arstall
                betegnelse {
                  kode
                }
              }
              kullStartTilTermin {
                id
                arstall
                betegnelse {
                  kode
                }
              }
              sisteTerminForValg {
                arstall
                betegnelse {
                  kode
                }
                id
              }
            }
            terminNummerRelativStart
            parent {
              studieoppbygningsdel {
                kode
              }
              rekkefolgenummer
            }
          }
        }
        cursor
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
  """
  for studieprogramkode in studieprogramkoder:
    #test om det finnes informasjon for det studieprogrammet det året:
    kontroll_variables = {"cursor": None, "studieprogramkode": studieprogramkode, "arstall": arstall, "betegnelse": terminbetegnelse}
    kontroll_result = run_query(query, username, password, kontroll_variables)
    if not kontroll_result['data']['studieoppbygninger']['edges']:
      continue 
    print(studieprogramkode,arstall)

    filnavn = f'''{studieprogramkode}-{arstall}{terminbetegnelse[0]}.html'''
    filbane = f'''c:/Users/tandr/Visual Studio Code/FS Grapql/studieløptabell/{filnavn}'''
    fil = {}
    # Variabel for å holde cursor
    cursor = None
    beskrivelse = []

    tabelldata = []
    
    # Hent alle sider med resultater
    while True:
        variables = {"cursor": None, "studieprogramkode": studieprogramkode, "arstall": arstall, "betegnelse": terminbetegnelse}
        result = run_query(query, username, password, variables)

        studieoppbygninger = result['data']['studieoppbygninger']
        
        alleOppbygningsdeler = studieoppbygninger['edges'][0]['node']['alleOppbygningsdeler']
        #print(alleOppbygningsdeler)
       
        for bygningsdel in alleOppbygningsdeler:
            parent = bygningsdel['studieoppbygningsdel']['kode']
            if bygningsdel['parent']:
                parent = bygningsdel['parent']['studieoppbygningsdel']['kode']
            #bygningsdel['parent']['rekkefolgenummer'] 
            emneKombTilKullTermin = 999999
            emneKombFraKullTermin = 1
            if bygningsdel['kullterminer']:
                if bygningsdel['kullterminer']['kullStartTilTermin']:
                    emneKombTilKullTermin = artermin(bygningsdel['kullterminer']['kullStartTilTermin']['arstall'], bygningsdel['kullterminer']['kullStartTilTermin']['betegnelse']['kode'])
                if bygningsdel['kullterminer']['kullStartFraTermin']:
                    emneKombFraKullTermin = artermin(bygningsdel['kullterminer']['kullStartFraTermin']['arstall'], bygningsdel['kullterminer']['kullStartFraTermin']['betegnelse']['kode'])

            if (int(programkullartermin) >= int(emneKombFraKullTermin)) and (int(programkullartermin) <= int(emneKombTilKullTermin)):
                        
                emneliste =  []
                for emner in bygningsdel['studieoppbygningsdel']['emner']:
                    emneTilKullTermin = 999999
                    emneFraKullTermin = 1
                    emner['sisteTerminForValgStatus']=''
                    if emner['kullterminer']:
                        if emner['kullterminer']['tilKullTermin']:
                            tilKullTerminArstall = emner['kullterminer']['tilKullTermin']['arstall']
                            tilKullTerminTermin = emner['kullterminer']['tilKullTermin']['betegnelse']['kode']
                            nyTilKullTermin = artermin(int(tilKullTerminArstall), tilKullTerminTermin)
                            emneTilKullTermin = nyTilKullTermin
                        if emner['kullterminer']['fraKullTermin']:
                            emneFraKullTermin = artermin(emner['kullterminer']['fraKullTermin']['arstall'], emner['kullterminer']['fraKullTermin']['betegnelse']['kode'])

                    if emner['sisteTerminForValg']:
                        sisteTerminForValg = artermin(emner['sisteTerminForValg']['arstall'],emner['sisteTerminForValg']['betegnelse']['kode'])
                        
                        if (int(innevartermin) >= int(sisteTerminForValg)):
                            emner['sisteTerminForValgStatus'] = 'Utgått'
                            
                    if (int(programkullartermin) >= int(emneFraKullTermin)) and (int(programkullartermin) <= int(emneTilKullTermin)):
                        emneliste.append(emner)

                
                emnekombinasjon = bygningsdel['studieoppbygningsdel']
                emnekombinasjon['eier'] = parent
                emnekombinasjon['frieEmnevalg']
                emnekombinasjon['kullStartFraTermin'] = ''
                emnekombinasjon['kullStartTilTermin'] = ''
                emnekombinasjon['sisteTerminForValg'] = ''
                emnekombinasjon['kullterminer']=bygningsdel['kullterminer']
                #emnekombinasjon['emner'] = []
                if bygningsdel['rekkefolgenummer'] is None:
                    emnekombinasjon['rekkefolgenummer']=0
                else:
                    emnekombinasjon['rekkefolgenummer']=bygningsdel['rekkefolgenummer']          
                
                emnekombinasjon['emner'] = emneliste
                
                tabelldata.append(emnekombinasjon)
            
            

          
        # Sjekk om det er flere sider
        if studieoppbygninger['pageInfo']['hasNextPage']:
            cursor = studieoppbygninger['pageInfo']['endCursor']
        else:
            break
    


    # Oppslagstabeller
    kode_til_element = {el['kode']: el for el in tabelldata}
    eier_til_barn = {}

    for el in tabelldata:
        if el['kode'] != el['eier']:  # Unngå sirkulær referanse
            eier_til_barn.setdefault(el['eier'], []).append(el['kode'])


    #filtrerer tabelldata for å fjerne emnekombinasjoner uten barn som ikke er frie emnevalg.
    tabelldata_filtrert = [
        el for el in tabelldata if el['emner'] or el['kode'] in eier_til_barn or el['kode'] == el['eier'] or el['frieEmnevalg']['begrensninger']
    ]
    
    tabelldata = tabelldata_filtrert

    # lag eier_til barn på nytt etter å ha filtrert ut emnekombinasjoner uten barn
    eier_til_barn = {}
    for el in tabelldata:
        if el['kode'] != el['eier']:  # Unngå sirkulær referanse
            eier_til_barn.setdefault(el['eier'], []).append(el['kode'])

    # Finn toppnivå-elementet (det som eier seg selv)
    rot_element = next(el for el in tabelldata if el['kode'] == el['eier'])
    

    # Finn nivået rekursivt
    def finn_nivå(kode, cache={}):
        if kode in cache:
            return cache[kode]
        if kode not in kode_til_element:  # Hvis elementet ikke finnes, antar vi nivå 0
            return 0
        eier = kode_til_element[kode]['eier']
        nivå = 0 if kode == eier else finn_nivå(eier, cache) + 1
        cache[kode] = nivå
        return nivå

    # Beregn nivåene
    for el in tabelldata:
        el['nivå'] = finn_nivå(el['kode'])


    def hent_rekkefolge(tabelldata, kode):
        # Bruk next() for å hente rekkefolge basert på kode
        return next((el['rekkefolgenummer'] for el in tabelldata if el['kode'] == kode), None)
    
    


    # Funksjon for rekursiv sortering
    def hierarkisk_sortering(kode):
        
        """Returnerer elementet og alle dets underordnede i riktig rekkefølge."""
        if kode not in kode_til_element:
            return []
        
        element = kode_til_element[kode]
        
        sortert_liste = [element]  # Start med seg selv
        
        # Finn og sorter barn etter nivå og kode
       
        barn = sorted(
            eier_til_barn.get(kode, []),
            key=lambda x: (finn_nivå(x), hent_rekkefolge(tabelldata, x), x)
        )
        for b in barn:
            sortert_liste.extend(hierarkisk_sortering(b))  # Legg til barn rekursivt
        
        return sortert_liste
    
    
    # Start sortering fra rot-elementet
    tabelldata_sortert = hierarkisk_sortering(rot_element['kode'])

    # Vis resultatet
    for idx, el in enumerate(tabelldata_sortert, 1):
        print(f"{idx}. {el['kode']}",f"{el['navnAlleSprak']['nb']}", f"(Nivå {el['nivå']})", f"(Rekkefolgenummer {el['rekkefolgenummer']})")
        
        if el['beskrivelseAlleSprak']:
            print('beskrivelse: ', el['beskrivelseAlleSprak']['nb'])
        if el['emner']:
            for emne in el['emner']:
                print(f"{idx}.", emne['emne']['kode'], f"{emne['emne']['vekting']['emnevekting']['verdi']} sp", emne['valgregel']['kode'], emne['rekkefolgenummer'], emne['terminForPlasseringIUtdanningsplan']['terminnummerForhandsvalgt'], emne['sisteTerminForValgStatus'])
        if el['frieEmnevalg']['begrensninger']:
            ''
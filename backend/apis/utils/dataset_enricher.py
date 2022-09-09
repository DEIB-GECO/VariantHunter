# se puoi mettere una colonna con la frequenza di sequenze con quel lineage e
# quella mutazione nel periodo 11-15 e 16-20

import csv
from os.path import exists
from types import SimpleNamespace

from apis.bulk_lineage_specific import extract_week_seq_counts, extract_specific_mutation_data
from apis.utils.bulk_analyzer import compute_weeks_from_date
from apis.utils.path_manager import create_directory

# ################## CONFIGURATION ##################
#     use math.inf or -math.inf to remove filters

c = {}
c['end_date'] = "2022-05-20"
c = SimpleNamespace(**c)


# ####################################################


def run_dataset_enricher():
    dir_name = 'dataset_enricher' + c.end_date.replace('-', '_')

    i = 0
    while exists(f"{i if i > 0 else ''}{dir_name}"):
        i += 1

    create_directory(f"{i if i > 0 else ''}{dir_name}")

    with open(f"{i if i > 0 else ''}{dir_name}/enriched_test.csv", 'w', encoding='UTF8') as f:
        fieldnames = ['location', 'lineage', 'protein_mut',
                      'col1','col2','col3','col4','col5','col6','col7','col8',
                      'freq_11_15','freq_16_20']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        with open('test2.csv', mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            line_count = 0
            for row in reader:
                lineage = row['lineage']
                location = row['location']
                protein_mut = row['protein_mut']
                protein, mut = protein_mut.split("_")

                print("\t\t> Location: "+location+", Lineage: " + lineage +", Mutation: "+protein_mut)
                w = compute_weeks_from_date(c.end_date)
                week_sequence_counts = extract_week_seq_counts(location, lineage, w)

                mut_w5, mut_w6 = extract_specific_mutation_data(location, lineage, protein_mut, w)

                tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4, tot_seq_w5, tot_seq_w6 = week_sequence_counts

                c5 = mut_w5.get(protein_mut, 0)
                c6 = mut_w6.get(protein_mut, 0)
                # print(c5,end=" ")
                # print(c6)

                f5 = (c5 / tot_seq_w5) * 100 if tot_seq_w5 > 0 else 0
                f6 = (c6 / tot_seq_w6) * 100 if tot_seq_w6 > 0 else 0

                print("\t\t\t> Period: " + str(w['w5_begin']) + " - " + str(w['w5_end']) + ": " + str(f5))
                print("\t\t\t> Period: " + str(w['w6_begin']) + " - " + str(w['w6_end']) + ": " + str(f6))

                row['freq_11_15']=f5
                row['freq_16_20'] = f6

                writer.writerow(row)
                line_count += 1

            print(f'Processed {line_count} lines.')

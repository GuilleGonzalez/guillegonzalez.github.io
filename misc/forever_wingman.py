import re # Regular Expressions
import pandas as pd
from bs4 import BeautifulSoup # Retrieve Visible Text (Non-HTML) on Web Pages
from time import perf_counter # perf_counter() Function for Timing
from playwright.sync_api import sync_playwright # Retrieve Dynamic JavaScript Website Contents

# Because the URLs are always in the same order,  the requirements CSV line up exactly with the main one.
URLS = 'https://foreverwingman.com/career_fields/1a1x2-mobility-force-aviator/,https://foreverwingman.com/career_fields/1a1x3-special-mission-aviator/,https://foreverwingman.com/career_fields/1a1x8-executive-mission-aviator/,https://foreverwingman.com/career_fields/1a3x1-airborne-mission-systems-operator/,https://foreverwingman.com/career_fields/1a8x1-airborne-cryptologic-language-analyst/,https://foreverwingman.com/career_fields/1a8x2-airborne-intelligence-surveillance-and-reconnaissance/,https://foreverwingman.com/career_fields/1b4x1-cyber-warfare-operations/,https://foreverwingman.com/career_fields/1c0x2-aviation-resource-management/,https://foreverwingman.com/career_fields/1c1x1-air-traffic-control/,https://foreverwingman.com/career_fields/1c3x1-command-control-operations/,https://foreverwingman.com/career_fields/1c5x1-command-and-control-battle-management-operations/,https://foreverwingman.com/career_fields/1c6x1-space-systems-operations/,https://foreverwingman.com/career_fields/1c7x1-airfield-management/,https://foreverwingman.com/career_fields/1c8x3-radar-airfield-weather-systems-raws-afsc/,https://foreverwingman.com/career_fields/1d7x1-cyber-defense-operations-afsc/,https://foreverwingman.com/career_fields/1d7x2-spectrum-defense-operations/,https://foreverwingman.com/career_fields/1d7x3-cable-and-antennae-defense-operations/,https://foreverwingman.com/career_fields/1h0x1-aerospace-physiology/,https://foreverwingman.com/career_fields/1n0x1-all-source-intelligence/,https://foreverwingman.com/career_fields/1n1x1-geospatial-intelligence-geoint/,https://foreverwingman.com/career_fields/1n2x1-signals-intelligence/,https://foreverwingman.com/career_fields/1n3x1-cryptologic-language-analyst/,https://foreverwingman.com/career_fields/1n4x1-cyber-intelligence/,https://foreverwingman.com/career_fields/1n4x2-cryptologic-language-analyst-reporter/,https://foreverwingman.com/career_fields/1n7x1-human-intelligence-specialist/,https://foreverwingman.com/career_fields/1n8x1-targeting-analyst/,https://foreverwingman.com/career_fields/1p0x1-aircrew-flight-equipment/,https://foreverwingman.com/career_fields/1s0x1-safety/,https://foreverwingman.com/career_fields/1t0x1-survival-evasion-resistance-and-escape-sere/,https://foreverwingman.com/career_fields/1u0x1-remotely-piloted-aircraft-rpa-sensor-operator/,https://foreverwingman.com/career_fields/1u1x1-remotely-piloted-aircraft-rpa-pilot/,https://foreverwingman.com/career_fields/1w0x1-weather/,https://foreverwingman.com/career_fields/1z1x1-pararescue/,https://foreverwingman.com/career_fields/1z2x1-combat-control/,https://foreverwingman.com/career_fields/1z3x1-tactical-air-control-party-tacp/,https://foreverwingman.com/career_fields/1z4x1-special-reconnaissance/,https://foreverwingman.com/career_fields/2a0x1-avionics-test-station-and-components/,https://foreverwingman.com/career_fields/2a2x1-special-operations-forces-personnel-recovery-integrated-communication-navigation-mission-systems/,https://foreverwingman.com/career_fields/2a2x2-special-operations-forces-personnel-recovery-sof-pr-integrated-instrument-and-flight-control-systems/,https://foreverwingman.com/career_fields/2a2x3-special-operations-forces-personnel-recovery-sof-pr-integrated-electronic-warfare-systems/,https://foreverwingman.com/career_fields/2a3x3-tactical-aircraft-maintenance/,https://foreverwingman.com/career_fields/2a3x4-fighter-aircraft-integrated-avionics/,https://foreverwingman.com/career_fields/2a3x5-advanced-fighter-aircraft-integrated-avionics/,https://foreverwingman.com/career_fields/2a3x7-tactical-aircraft-maintenance-5th-generation/,https://foreverwingman.com/career_fields/2a3x8-remotely-piloted-aircraft-maintenance/,https://foreverwingman.com/career_fields/2a5x1-airlift-special-mission-aircraft-maintenance/,https://foreverwingman.com/career_fields/2a5x2-helicopter-tiltrotor-aircraft-maintenance/,https://foreverwingman.com/career_fields/2a5x4-refuel-bomber-aircraft-maintenance/,https://foreverwingman.com/career_fields/2a6x1-aerospace-propulsion/,https://foreverwingman.com/career_fields/2a6x2-aerospace-ground-equipment-age/,https://foreverwingman.com/career_fields/2a6x3-aircrew-egress-systems/,https://foreverwingman.com/career_fields/2a6x4-aircraft-fuel-systems/,https://foreverwingman.com/career_fields/2a6x5-aircraft-hydraulic-systems/,https://foreverwingman.com/career_fields/2a6x6-aircraft-electrical-and-environmental-systems/,https://foreverwingman.com/career_fields/2a7x1-aircraft-metals-technology/,https://foreverwingman.com/career_fields/2a7x2-nondestructive-inspection/,https://foreverwingman.com/career_fields/2a7x3-aircraft-structural-maintenance/,https://foreverwingman.com/career_fields/2a7x5-low-observable-aircraft-structural-maintenance/,https://foreverwingman.com/career_fields/2a8x1-mobility-air-forces-integrated-communication-navigation-mission-systems/,https://foreverwingman.com/career_fields/2a8x2-mobility-air-forces-integrated-instrument-and-flight-control-systems/,https://foreverwingman.com/career_fields/2a9x1-bomber-special-integrated-communication-navigation-mission-systems/,https://foreverwingman.com/career_fields/2a9x2-bomber-special-integrated-instrument-and-flight-control-systems/,https://foreverwingman.com/career_fields/2a9x3-bomber-special-electronic-warfare-and-radar-surveillance-integrated-avionics/,https://foreverwingman.com/career_fields/2f0x1-fuels/,https://foreverwingman.com/career_fields/2g0x1-logistics-plans/,https://foreverwingman.com/career_fields/2m0x1-missile-and-space-systems-electronic-maintenance/,https://foreverwingman.com/career_fields/2m0x2-missile-and-space-systems-maintenance/,https://foreverwingman.com/career_fields/2m0x3-missile-and-space-facilities/,https://foreverwingman.com/career_fields/2p0x1-precision-measurement-equipment-laboratory/,https://foreverwingman.com/career_fields/2r0x1-maintenance-management-analysis/,https://foreverwingman.com/career_fields/2r1x1-maintenance-management-production/,https://foreverwingman.com/career_fields/2s0x1-materiel-management/,https://foreverwingman.com/career_fields/2t0x1-traffic-management/,https://foreverwingman.com/career_fields/2t1x1-ground-transportation/,https://foreverwingman.com/career_fields/2t2x1-air-transportation/,https://foreverwingman.com/career_fields/2t3x1-mission-generation-vehicular-equipment-maintenance/,https://foreverwingman.com/career_fields/2t3x7-fleet-management-and-analysis/,https://foreverwingman.com/career_fields/2w0x1-munitions-systems/,https://foreverwingman.com/career_fields/2w1x1-aircraft-armament-systems/,https://foreverwingman.com/career_fields/2w2x1-nuclear-weapons/,https://foreverwingman.com/career_fields/3e0x2-electrical-power-production/,https://foreverwingman.com/career_fields/3e0x2-electrical-power-production/,https://foreverwingman.com/career_fields/3e1x1-heating-ventilation-air-conditioning-and-refrigeration/,https://foreverwingman.com/career_fields/3e2x1-pavements-and-construction-equipment/,https://foreverwingman.com/career_fields/3e3x1-structural/,https://foreverwingman.com/career_fields/3e4x1-water-and-fuel-systems-maintenance/,https://foreverwingman.com/career_fields/3e4x3-pest-management/,https://foreverwingman.com/career_fields/3e5x1-engineering/,https://foreverwingman.com/career_fields/3e6x1-operations-management/,https://foreverwingman.com/career_fields/3e7x1-fire-protection/,https://foreverwingman.com/career_fields/3e8x1-explosive-ordnance-disposal-eod/,https://foreverwingman.com/career_fields/3e9x1-emergency-management/,https://foreverwingman.com/career_fields/3f0x1-personnel/,https://foreverwingman.com/career_fields/3f1x1-services/,https://foreverwingman.com/career_fields/3f2x1-education-and-training/,https://foreverwingman.com/career_fields/3f3x1-manpower/,https://foreverwingman.com/career_fields/3f4x1-equal-opportunity/,https://foreverwingman.com/career_fields/3f5x1-administration/,https://foreverwingman.com/career_fields/3g0x1-talent-acqusition/,https://foreverwingman.com/career_fields/3h0x1-historian/,https://foreverwingman.com/career_fields/3n0x6-public-affairs/,https://foreverwingman.com/career_fields/3n1x1-regional-band/,https://foreverwingman.com/career_fields/3n2x1-premier-band/,https://foreverwingman.com/career_fields/3n3x1-premier-band-the-usaf-academy-band/,https://foreverwingman.com/career_fields/3p0x1-security-forces/,https://foreverwingman.com/career_fields/4a0x1-health-services-management/,https://foreverwingman.com/career_fields/4a1x1-medical-materiel/,https://foreverwingman.com/career_fields/4a2x1-biomedical-equipment/,https://foreverwingman.com/career_fields/4b0x1-bioenvironmental-engineering/,https://foreverwingman.com/career_fields/4c0x1-mental-health-service/,https://foreverwingman.com/career_fields/4d0x1-diet-therapy/,https://foreverwingman.com/career_fields/4e0x1-public-health/,https://foreverwingman.com/career_fields/4h0x1-cardiopulmonary-laboratory/,https://foreverwingman.com/career_fields/4j0x2-physical-medicine/,https://foreverwingman.com/career_fields/4n0x1-aerospace-medical-service/,https://foreverwingman.com/career_fields/4n1x1-surgical-service/,https://foreverwingman.com/career_fields/4p0x1-pharmacy/,https://foreverwingman.com/career_fields/4r0x1-diagnostic-imaging/,https://foreverwingman.com/career_fields/4t0x1-medical-laboratory/,https://foreverwingman.com/career_fields/4t0x2-histopathology/,https://foreverwingman.com/career_fields/4v0x1-ophthalmic/,https://foreverwingman.com/career_fields/4y0x1-dental-assistant/,https://foreverwingman.com/career_fields/4y0x2-dental-laboratory/,https://foreverwingman.com/career_fields/5j0x1-paralegal/,https://foreverwingman.com/career_fields/5r0x1-religious-affairs/,https://foreverwingman.com/career_fields/6c0x1-contracting/,https://foreverwingman.com/career_fields/6f0x1-financial-management-comptroller/,https://foreverwingman.com/career_fields/7s0x1-special-investigations/,https://foreverwingman.com/career_fields/8a200-enlisted-aide/,https://foreverwingman.com/career_fields/8a300-protocol/,https://foreverwingman.com/career_fields/8a400-talent-management-consultant/,https://foreverwingman.com/career_fields/8b000-military-training-instructor-mti/,https://foreverwingman.com/career_fields/8b100-military-training-leader-mtl/,https://foreverwingman.com/career_fields/8b200-academy-military-training-nco/,https://foreverwingman.com/career_fields/8b300-afrotc-training-instructor/,https://foreverwingman.com/career_fields/8c000-military-and-family-readiness-non-commissioned-officer/,https://foreverwingman.com/career_fields/8d100-language-and-culture-advisor/,https://foreverwingman.com/career_fields/8f000-first-sergeant/,https://foreverwingman.com/career_fields/8g000-premier-honor-guard/,https://foreverwingman.com/career_fields/8g100-base-honor-guard-program-manager/,https://foreverwingman.com/career_fields/8h000-airmen-dorm-leader/,https://foreverwingman.com/career_fields/8i000-inspector-general-superintendent/,https://foreverwingman.com/career_fields/8i100-inspections-coordinator/,https://foreverwingman.com/career_fields/8i200-complaints-and-resolution-coordinator/,https://foreverwingman.com/career_fields/8k000-software-development-specialist/,https://foreverwingman.com/career_fields/8l100-enlisted-air-advisor-basic/,https://foreverwingman.com/career_fields/8l400-enlisted-air-advisor-advanced/,https://foreverwingman.com/career_fields/8l700-enlisted-combat-aviation-advisor-sof/,https://foreverwingman.com/career_fields/8p000-courier/,https://foreverwingman.com/career_fields/8p100-defense-attache/,https://foreverwingman.com/career_fields/8r000-enlisted-accessions-recruiter/,https://foreverwingman.com/career_fields/8r200-second-tier-recruiter/,https://foreverwingman.com/career_fields/8r300-third-tier-recruiter/,https://foreverwingman.com/career_fields/8s000-missile-facility-manager/,https://foreverwingman.com/career_fields/8s200-combat-crew-communications/,https://foreverwingman.com/career_fields/8t000-professional-military-education-instructor/,https://foreverwingman.com/career_fields/8t100-enlisted-professional-military-education-instructional-system/,https://foreverwingman.com/career_fields/8t200-development-advisor/,https://foreverwingman.com/career_fields/8u000-unit-deployment-manager/,https://foreverwingman.com/career_fields/8u100-weapons-of-mass-destruction-civil-support-team-wmd-cst/,https://foreverwingman.com/career_fields/8w000-weapons-safety-manager-wing-level/,https://foreverwingman.com/career_fields/8y000-pathfinder/'.split(',')


def main():
    get_main_csv()
    get_requirements_csv()


def get_main_csv(output_path: str = 'afsc_wingman.csv'):
    def extract_info(s: str, url: str, verbose: bool = False) -> dict:
        # Extract the AFSC and AFSC Title
        afsc_title = s[:s.find(" AFSC")].replace('–', '-')
        if verbose: print(f"\n\n{afsc_title}")

        # Extract text between "Days:" and "Locations:"
        days_match = re.search(r'Days:\s*(.*?)(?=Locations:)', s)
        days_text = days_match.group(1).strip() if days_match else ''
        if verbose: print(f"Technical School Days: {days_text}")

        # Extract text between "Locations:" and "Other"
        locations_match = re.search(r'Locations:\s*(.*?)(?=Other)', s)
        locations_text = locations_match.group(1).strip() if locations_match else ''
        if verbose: print(f"Locations: {locations_text}")

        # Extract text between "4-Year Bonus:"" and "6-Year"
        four_year_bonus_match = re.search(r'4-Year Bonus:\s*(.*?)(?=6-Year)', s)
        four_year_bonus_text = four_year_bonus_match.group(1).strip() if four_year_bonus_match else 'None'
        if verbose: print(f"4-Year Bonus: {four_year_bonus_text}")

        # Extract text between "6-Year Bonus:" and "Badge"
        six_year_bonus_match = re.search(r'6-Year Bonus:\s*(.*?)(?=Badge)', s)
        six_year_bonus_text = six_year_bonus_match.group(1).strip() if six_year_bonus_match else 'None'
        if verbose: print(f"6-Year Bonus: {six_year_bonus_text}")

        # Extract text between "Clearance" and "Open"
        clearance_text_match = re.search(r'Clearance(.*?)(?=Open)', s)
        clearance_text = clearance_text_match.group(1).strip() if clearance_text_match else ''
        if verbose: print(f"Clearance: {clearance_text}")

        # Extract text between "Open Aptitude Category" and "AFSC"
        aptitude_match = re.search(r'Open Aptitude Category(.*?)(?=AFSC)', s)
        aptitude_text = aptitude_match.group(1).strip() if aptitude_match else ''
        if verbose: print(f"Open Aptitude Category: {aptitude_text}")

        # Extract text starting after "Demographics" checking for the specifics of "Males:", "Females:", and "Total:"
        demographics_match = re.search(r'Demographics(?:\s*(Males:\s*\d+))?(?:\s*(Females:\s*\d+))?(?:\s*(Total:\s*\d+))?', s)
        males_text, females_text, total_text = '', '', ''
        if demographics_match:
            males_text = demographics_match.group(1) or ''
            females_text = demographics_match.group(2) or ''
            total_text = demographics_match.group(3) or ''
        if verbose: print(f"Demographics -> {males_text}  {females_text}  {total_text}")

        # Extract the first High Salary
        high_salary_match = re.search(r'High Salary:\s*\$([\d,]+)', s)
        high_salary = f"${high_salary_match.group(1)}" if high_salary_match else ''
        if verbose: print(f"First High Salary: {high_salary}")

        # Extract the first Low Salary
        low_salary_match = re.search(r'Low Salary:\s*\$([\d,]+)', s)
        low_salary = f"${low_salary_match.group(1)}" if low_salary_match else ''
        if verbose: print(f"First Low Salary: {low_salary}")
        if verbose: print(url)
        
        # print([afsc_title, days_text, locations_text, four_year_bonus_text, six_year_bonus_text, clearance_text, aptitude_text, males_text.removeprefix('Males: '), females_text.removeprefix('Females: '), total_text.removeprefix('Total: '), high_salary, low_salary])
        return {
            'AFSC_Title': afsc_title,
            'Tech_School_Days': days_text,
            'Training_Location': locations_text,
            '4-Year_Bonus': four_year_bonus_text.removeprefix('$').replace(',', ''),
            '6-Year_Bonus': six_year_bonus_text.removeprefix('$').replace(',', ''),
            'Clearance': clearance_text,
            'Open_Aptitude_Area': aptitude_text.replace('and', '&'),
            'Males': males_text.removeprefix('Males: '),
            'Females': females_text.removeprefix('Females: '),
            'Total_People': total_text.removeprefix('Total: '),
            'High_Salary': high_salary.removeprefix('$').replace(',', ''),
            'Low_Salary': low_salary.removeprefix('$').replace(',', ''),
            'URL': url.strip()
        }

    print(f'Creating "{output_path}"...')
    start_time, data = perf_counter(), []
    for i, url in enumerate(URLS):
        with sync_playwright() as playwright:
            contents = run_playwright(playwright, url) 
        data.append(extract_info(contents, url)) 
        print(f'URL {i+1} of {len(URLS)} Completed ({url.strip()})')
    pd.DataFrame(data).to_csv(output_path, index=False)
    print(f'Successfully Created "{output_path}" in {(perf_counter() - start_time):.2f} Seconds\n')


def get_requirements_csv(output_path: str = 'afsc_wingman_requirements.csv'):
    def extract_info(s: str, url: str) -> str:
        match = re.search(r'Testing\s*(.*?)(?=GeneralMust)', s)
        data = match.group(1).strip() if match else ''

        replacements = {
            'Mechanical - ': 'M',
            'Administrative - ':'A',
            'General - ': 'G',
            'Electrical - ': 'E',
            'and': '+',
            'OR': ' or ',
            'PSM - ' : 'PSM',
            'Cyber - ': 'Cyber'  
        }

        for old, new in replacements.items():
            data = data.replace(old, new)
        overall_requirement, area1, score1, area2, score2, alternative_requirement = data, '', '', '', '', ''
        data = data.replace('Cyber', 'C').replace('PSM', 'P')

        if len(data) > 0 and data[0] in ('M', 'A', 'G', 'E', 'P', 'C'): area1, score1, = data[0], data[1:3]
        if len(data) > 3 and data[3:6] == ' + ': area2, score2 = data[6], data[7:9]
        if ' or ' in data: alternative_requirement = data[data.find(' or ')+4:]

        return f'{overall_requirement},{area1},{score1},{area2},{score2},{alternative_requirement},{url}\n'


    print(f'Creating "{output_path}"...')
    start_time = perf_counter()
    with open(output_path, 'w') as output:
        output.write('Overall_Requirements,Area1,Score1,Area2,Score2,ALT_Reqs,AFSC_Reqs_URL\n')
        for i, url in enumerate(URLS):
            requirements_url = f'{url.strip()}{url[41:46]}-entry-requirements/'
            with sync_playwright() as playwright:
                contents = run_playwright(playwright, requirements_url)
            output.write(extract_info(contents, requirements_url))
            print(f'URL {i+1} of {len(URLS)} Completed ({requirements_url})')
    print(f'Successfully Created "{output_path}" in {(perf_counter() - start_time):.2f} Seconds\n')


def run_playwright(playwright, url: str) -> str:
    browser = playwright.chromium.launch(headless=True, args=["--disable-extensions", "--disable-gpu", "--no-sandbox"])
    page = browser.new_page()

    def block_non_essential_requests(route, request):
        if request.resource_type in ["image", "stylesheet", "font", "media"]: route.abort()  
        else: route.continue_()
    page.route("**/*", block_non_essential_requests)

    page.goto(url, wait_until='domcontentloaded') # Go to the URL Passed into this Function [The wait_until='documentloaded' tries to speed up the code by not waiting for all the CSS or JS to load as well]
    content = page.content() # The "content" Variable Now Contains All the HTML for the Site
    browser.close()

    soup = BeautifulSoup(content, 'html.parser') # Set a Temproary "soup" BeutifulSoup Object to Parse the HTML (of "content")
    return soup.get_text(strip=True) # Return the Visible Text from the Website [strip=True Ignores New Lines to Avoid Tons of Blank Lines & So the Returned String is a One-Line String (albiet long)]


if __name__ == '__main__': 
    main()

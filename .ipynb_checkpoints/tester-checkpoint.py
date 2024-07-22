import unittest
import json
from vision_parser import process_images  
import os

class TestAdProcessing(unittest.TestCase):

    def setUp(self):
        #  mocked to return a predefined set of ads
        self.mock_process_images = lambda x: self.get_mock_processed_ads()

    def get_mock_processed_ads(self):
        return {
            "ads": [
                {
                    "company": "Gaia Herbs",
                    "library_id": "1146296186451945",
                    "active": True,
                    "started": "Jul 19, 2024",
                    "platforms": ["Facebook", "Instagram", "Audience Network", "Messenger"],
                    "text": "Enhance your journey with herbal supplements designed to nurture your body at all stages of motherhood. Discover natural support for fertility, pregnancy & healthy lactation.*\n\n*This statement has not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.",
                    "discount": "n/a"
                },
                {
                    "company": "Gaia Herbs",
                    "library_id": "2102791643440245",
                    "active": True,
                    "started": "Jul 19, 2024",
                    "platforms": ["Facebook", "Instagram", "Audience Network", "Messenger"],
                    "text": "Navigate the changes of menopause with confidence and comfort. Gaia Herbs Menopause Support Daytime is crafted with a blend of Vitex, Black Cohosh, St. John's Wort, and Oats to help maintain healthy hormone balance and well-being*. This natural formula is designed to ease symptoms like hot flashes and irritability, supporting you through every stage of menopause*.",
                    "discount": "n/a"
                },
                {
                    "company": "Gaia Herbs",
                    "library_id": "808037064798757",
                    "active": True,
                    "started": "Jul 2, 2024",
                    "platforms": ["Facebook", "Instagram"],
                    "text": "Stressed out? Reishi to the rescue*. Healthy liver function support? Try turkey tail*. Brain fog? Lion's mane is your friend*.\n\nOur Certified USDA Organic mushrooms are purity-tested, extracted, and free of grains, starches, and mycelium. So, you get just the mushroom and all its benefits.",
                    "discount": "n/a"
                },
                {
                    "company": "Gaia Herbs",
                    "library_id": "1967859000186946",
                    "active": False,
                    "started": "Nov 8, 2018",
                    "platforms": ["Facebook"],
                    "text": "This content was removed because it didn't follow our Advertising Standards.",
                    "discount": "n/a"
                }
            ]
        }

    def test_ad_processing(self):
        # Process  mock images
        result = self.mock_process_images([])  # Empty list as we're not actually processing images

        # Check correct number of ads
        self.assertEqual(len(result['ads']), 41, "Should have processed 41 ads")

        # expected library IDs
        expected_ids = [
            "1146296186451945", "2102791643440245", "1906054223244112",
            "282702484901205", "363616233208857", "1022576402542646",
            "1038379087699100", "1225578328876085", "893260642839681",
            "1907644746366167", "460515410118491", "1809325283208336",
            "322328837613685", "364721756723034", "433678066321435",
            "446493431483896", "459375733553386", "776885727966000",
            "780540130945005", "808037064798757", "808343531430614",
            "844050840965512", "921897826638665", "1011059403928857",
            "1057151615919784", "1531590857763771", "3781030948826043",
            "1003419197840034", "379812574685480", "404993215234563",
            "449625844530465", "1009401160799853", "759308449614337",
            "447831161355630", "26924707277128073", "1012501020578058",
            "1125783105316586", "381862578160378", "373570383511734",
            "306359060002576", "1967859000186946"
        ]

        # Check if all library IDs are present
        processed_ids = [ad['library_id'] for ad in result['ads']]
        for expected_id in expected_ids:
            self.assertIn(expected_id, processed_ids, f"Library ID {expected_id} not found in processed ads")

        # Check if all processed library IDs are expected
        for processed_id in processed_ids:
            self.assertIn(processed_id, expected_ids, f"Unexpected library ID {processed_id} found in processed ads")

        for ad in result['ads']:
            self.assertIn(ad['library_id'], expected_ids, f"Unexpected library ID {ad['library_id']} found")
            self.assertIsInstance(ad['company'], str)
            self.assertIsInstance(ad['active'], bool)
            self.assertIsInstance(ad['started'], str)
            self.assertIsInstance(ad['platforms'], list)
            self.assertIsInstance(ad['text'], str)
            self.assertIsInstance(ad['discount'], str)

        #specific active ad
        ad_808037064798757 = next(ad for ad in result['ads'] if ad['library_id'] == "808037064798757")
        self.assertEqual(ad_808037064798757['company'], "Gaia Herbs")
        self.assertTrue(ad_808037064798757['active'])
        self.assertEqual(ad_808037064798757['started'], "Jul 2, 2024")
        self.assertIn("Facebook", ad_808037064798757['platforms'])
        self.assertIn("Stressed out? Reishi to the rescue", ad_808037064798757['text'])
        self.assertEqual(ad_808037064798757['discount'], "n/a")

        # speific inactive ad
        ad_1967859000186946 = next(ad for ad in result['ads'] if ad['library_id'] == "1967859000186946")
        self.assertFalse(ad_1967859000186946['active'])
        self.assertEqual(ad_1967859000186946['started'], "Nov 8, 2018")
        self.assertIn("This content was removed", ad_1967859000186946['text'])


    def test_output_file_creation(self):
        # Run the main script (you might need to modify this part)
        import vision_parser
        
        # Check if the output file exists
        self.assertTrue(os.path.exists("processed_ads.json"), "Output file should be created")
        
        # Read and check the contents of the output file
        with open("processed_ads.json", 'r') as f:
            data = json.load(f)
        
        self.assertIn('ads', data, "Output should have an 'ads' key")
        print(data['ads'])
        self.assertEqual(len(data['ads']), 41, "Output should contain 41 ads")

if __name__ == '__main__':
    unittest.main()
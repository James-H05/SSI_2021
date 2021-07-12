{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "ee_data.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/James-H05/SSI_2021/blob/main/ee_data.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "0nnHSLCSVh1D"
      },
      "source": [
        "# import earth engine library - should be installed already in colab\n",
        "import ee"
      ],
      "execution_count": 2,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "--HPrXodaevU",
        "outputId": "093be2e9-3c12-4107-c023-531f6400bc78"
      },
      "source": [
        "# Trigger the authentication flow.\n",
        "ee.Authenticate()\n",
        "\n",
        "# Initialize the library.\n",
        "ee.Initialize()"
      ],
      "execution_count": 3,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "To authorize access needed by Earth Engine, open the following URL in a web browser and follow the instructions. If the web browser does not start automatically, please manually browse the URL below.\n",
            "\n",
            "    https://accounts.google.com/o/oauth2/auth?client_id=517222506229-vsmmajv00ul0bs7p89v5m89qs8eb9359.apps.googleusercontent.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fearthengine+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdevstorage.full_control&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&code_challenge=HP9j_UjB5S8RBbYeNjaPo9Vb_OuVB9pHI_-QD9PLeTM&code_challenge_method=S256\n",
            "\n",
            "The authorization workflow will generate a code, which you should paste in the box below. \n",
            "Enter verification code: 4/1AX4XfWggBQHkHMK1IFNZAM81k8NepgZLUs1AOgXQIS9FUxtcgaa1nAWvqIU\n",
            "\n",
            "Successfully saved authorization token.\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Fp4rdpy0eGjx",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 441
        },
        "outputId": "f149b7b9-31e3-4dfa-dcd3-0c5ae15d57e8"
      },
      "source": [
        "years = ['1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']\n",
        "months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']\n",
        "layers = ['aet', 'def', 'pdsi', 'pet', 'pr', 'ro', 'soil', 'srad', 'swe', 'tmmn', 'tmmx', 'vap', 'vpd', 'vs']\n",
        "countries = ['Austria', 'Belgium', 'Bulgaria', 'Switzerland', 'Cyprus', 'Czech Republic', 'Germany', 'Denmark', 'Estonia', 'Spain', 'Finland', 'France', 'Greece', 'Croatia', 'Hungary', 'Ireland', 'Italy', 'Lithuania', 'Luxemborg', 'Latvia', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Sweden', 'Slovenia', 'Slovakia', 'United Kingdom']\n",
        "\n",
        "csv = {}\n",
        "\n",
        "for country in countries:\n",
        "  for layer in layers:\n",
        "    csv[country + '_' + layer] = []\n",
        "\n",
        "for year_index in range(len(years)):\n",
        "  for month_index in range(len(months)):\n",
        "    for country in countries:\n",
        "\n",
        "      if(not (year_index == len(years) and month_index == len(months))):\n",
        "        start_date = years[year_index] + '-' + months[month_index] + '-01'\n",
        "        if(months[month_index] != '12'):\n",
        "          end_date = years[year_index] + '-' + months[month_index+1] + '-01'\n",
        "        else: # if december\n",
        "          end_date = years[year_index+1] + '-' + months[0] + '-01'\n",
        "\n",
        "        #TODO make sure it doesn't crash on the very last month\n",
        "\n",
        "        terraclimate = ee.ImageCollection(\"IDAHO_EPSCOR/TERRACLIMATE\").filter(ee.Filter.date(start_date, end_date)).first()\n",
        "        borders = ee.Feature(ee.FeatureCollection('FAO/GAUL/2015/level0').filter(ee.Filter.eq('ADM0_NAME', country)).first())\n",
        "\n",
        "        # Reduce the region. The region parameter is the Feature geometry.\n",
        "        meanDictionary = terraclimate.reduceRegion(\n",
        "          ee.Reducer.mean(),\n",
        "          geometry=borders.geometry(),\n",
        "          scale=30,\n",
        "          maxPixels=100000000,\n",
        "          bestEffort=True\n",
        "        )\n",
        "\n",
        "\n",
        "        # The result is a Dictionary.  Print it.\n",
        "        #print(country, start_date, \":\", meanDictionary.getInfo())\n",
        "        meanDictionary.getInfo()\n",
        "        \n",
        "        for layer in layers:\n",
        "          csv[country + '_' + layer].append(meanDictionary.getInfo()[layer])"
      ],
      "execution_count": 8,
      "outputs": [
        {
          "output_type": "error",
          "ename": "KeyboardInterrupt",
          "evalue": "ignored",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mTypeError\u001b[0m                                 Traceback (most recent call last)",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/urllib3/connectionpool.py\u001b[0m in \u001b[0;36m_make_request\u001b[0;34m(self, conn, method, url, timeout, chunked, **httplib_request_kw)\u001b[0m\n\u001b[1;32m    376\u001b[0m             \u001b[0;32mtry\u001b[0m\u001b[0;34m:\u001b[0m  \u001b[0;31m# Python 2.7, use buffering of HTTP responses\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 377\u001b[0;31m                 \u001b[0mhttplib_response\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mconn\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mgetresponse\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mbuffering\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;32mTrue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    378\u001b[0m             \u001b[0;32mexcept\u001b[0m \u001b[0mTypeError\u001b[0m\u001b[0;34m:\u001b[0m  \u001b[0;31m# Python 3\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mTypeError\u001b[0m: getresponse() got an unexpected keyword argument 'buffering'",
            "\nDuring handling of the above exception, another exception occurred:\n",
            "\u001b[0;31mKeyboardInterrupt\u001b[0m                         Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-8-0de9cc963f02>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m()\u001b[0m\n\u001b[1;32m     41\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     42\u001b[0m         \u001b[0;32mfor\u001b[0m \u001b[0mlayer\u001b[0m \u001b[0;32min\u001b[0m \u001b[0mlayers\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 43\u001b[0;31m           \u001b[0mcsv\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0mcountry\u001b[0m \u001b[0;34m+\u001b[0m \u001b[0;34m'_'\u001b[0m \u001b[0;34m+\u001b[0m \u001b[0mlayer\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mappend\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mmeanDictionary\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mgetInfo\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0mlayer\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/ee/computedobject.py\u001b[0m in \u001b[0;36mgetInfo\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m     96\u001b[0m       \u001b[0mThe\u001b[0m \u001b[0mobject\u001b[0m \u001b[0mcan\u001b[0m \u001b[0mevaluate\u001b[0m \u001b[0mto\u001b[0m \u001b[0manything\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     97\u001b[0m     \"\"\"\n\u001b[0;32m---> 98\u001b[0;31m     \u001b[0;32mreturn\u001b[0m \u001b[0mdata\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mcomputeValue\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     99\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    100\u001b[0m   \u001b[0;32mdef\u001b[0m \u001b[0mencode\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mencoder\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/ee/data.py\u001b[0m in \u001b[0;36mcomputeValue\u001b[0;34m(obj)\u001b[0m\n\u001b[1;32m    676\u001b[0m           \u001b[0mbody\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;34m{\u001b[0m\u001b[0;34m'expression'\u001b[0m\u001b[0;34m:\u001b[0m \u001b[0mserializer\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mencode\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mobj\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mfor_cloud_api\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;32mTrue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m}\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    677\u001b[0m           \u001b[0mproject\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0m_get_projects_path\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 678\u001b[0;31m           prettyPrint=False))['result']\n\u001b[0m\u001b[1;32m    679\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    680\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/ee/data.py\u001b[0m in \u001b[0;36m_execute_cloud_call\u001b[0;34m(call, num_retries)\u001b[0m\n\u001b[1;32m    332\u001b[0m   \"\"\"\n\u001b[1;32m    333\u001b[0m   \u001b[0;32mtry\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 334\u001b[0;31m     \u001b[0;32mreturn\u001b[0m \u001b[0mcall\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mexecute\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mnum_retries\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mnum_retries\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    335\u001b[0m   \u001b[0;32mexcept\u001b[0m \u001b[0mgoogleapiclient\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0merrors\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mHttpError\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0me\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    336\u001b[0m     \u001b[0;32mraise\u001b[0m \u001b[0m_translate_cloud_exception\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0me\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/googleapiclient/_helpers.py\u001b[0m in \u001b[0;36mpositional_wrapper\u001b[0;34m(*args, **kwargs)\u001b[0m\n\u001b[1;32m    132\u001b[0m                 \u001b[0;32melif\u001b[0m \u001b[0mpositional_parameters_enforcement\u001b[0m \u001b[0;34m==\u001b[0m \u001b[0mPOSITIONAL_WARNING\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    133\u001b[0m                     \u001b[0mlogger\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mwarning\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mmessage\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 134\u001b[0;31m             \u001b[0;32mreturn\u001b[0m \u001b[0mwrapped\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m*\u001b[0m\u001b[0margs\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0mkwargs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    135\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    136\u001b[0m         \u001b[0;32mreturn\u001b[0m \u001b[0mpositional_wrapper\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/googleapiclient/http.py\u001b[0m in \u001b[0;36mexecute\u001b[0;34m(self, http, num_retries)\u001b[0m\n\u001b[1;32m    907\u001b[0m             \u001b[0mmethod\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mstr\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mmethod\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    908\u001b[0m             \u001b[0mbody\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mbody\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 909\u001b[0;31m             \u001b[0mheaders\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mheaders\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    910\u001b[0m         )\n\u001b[1;32m    911\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/googleapiclient/http.py\u001b[0m in \u001b[0;36m_retry_request\u001b[0;34m(http, num_retries, req_type, sleep, rand, uri, method, *args, **kwargs)\u001b[0m\n\u001b[1;32m    175\u001b[0m         \u001b[0;32mtry\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    176\u001b[0m             \u001b[0mexception\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 177\u001b[0;31m             \u001b[0mresp\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mcontent\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mhttp\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mrequest\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0muri\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mmethod\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m*\u001b[0m\u001b[0margs\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0mkwargs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    178\u001b[0m         \u001b[0;31m# Retry on SSL errors and socket timeout errors.\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    179\u001b[0m         \u001b[0;32mexcept\u001b[0m \u001b[0m_ssl_SSLError\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mssl_error\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/google_auth_httplib2.py\u001b[0m in \u001b[0;36mrequest\u001b[0;34m(self, uri, method, body, headers, **kwargs)\u001b[0m\n\u001b[1;32m    199\u001b[0m         \u001b[0;31m# Make the request.\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    200\u001b[0m         response, content = self.http.request(\n\u001b[0;32m--> 201\u001b[0;31m             uri, method, body=body, headers=request_headers, **kwargs)\n\u001b[0m\u001b[1;32m    202\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    203\u001b[0m         \u001b[0;31m# If the response indicated that the credentials needed to be\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/httplib2/__init__.py\u001b[0m in \u001b[0;36mrequest\u001b[0;34m(self, uri, method, body, headers, redirections, connection_type)\u001b[0m\n\u001b[1;32m   1989\u001b[0m                         \u001b[0mheaders\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1990\u001b[0m                         \u001b[0mredirections\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 1991\u001b[0;31m                         \u001b[0mcachekey\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   1992\u001b[0m                     )\n\u001b[1;32m   1993\u001b[0m         \u001b[0;32mexcept\u001b[0m \u001b[0mException\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0me\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/httplib2/__init__.py\u001b[0m in \u001b[0;36m_request\u001b[0;34m(self, conn, host, absolute_uri, request_uri, method, body, headers, redirections, cachekey)\u001b[0m\n\u001b[1;32m   1649\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1650\u001b[0m         (response, content) = self._conn_request(\n\u001b[0;32m-> 1651\u001b[0;31m             \u001b[0mconn\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mrequest_uri\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mmethod\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mbody\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mheaders\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   1652\u001b[0m         )\n\u001b[1;32m   1653\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/httplib2shim/__init__.py\u001b[0m in \u001b[0;36m_conn_request\u001b[0;34m(self, conn, request_uri, method, body, headers)\u001b[0m\n\u001b[1;32m    146\u001b[0m                 \u001b[0mretries\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0murllib3\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mRetry\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mtotal\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;32mFalse\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mredirect\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;36m0\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    147\u001b[0m                 \u001b[0mtimeout\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0murllib3\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mTimeout\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mtotal\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mtimeout\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 148\u001b[0;31m                 decode_content=decode)\n\u001b[0m\u001b[1;32m    149\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    150\u001b[0m             \u001b[0mresponse\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0m_map_response\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0murllib3_response\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mdecode\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mdecode\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/urllib3/request.py\u001b[0m in \u001b[0;36mrequest\u001b[0;34m(self, method, url, fields, headers, **urlopen_kw)\u001b[0m\n\u001b[1;32m     70\u001b[0m             return self.request_encode_body(method, url, fields=fields,\n\u001b[1;32m     71\u001b[0m                                             \u001b[0mheaders\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mheaders\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 72\u001b[0;31m                                             **urlopen_kw)\n\u001b[0m\u001b[1;32m     73\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     74\u001b[0m     def request_encode_url(self, method, url, fields=None, headers=None,\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/urllib3/request.py\u001b[0m in \u001b[0;36mrequest_encode_body\u001b[0;34m(self, method, url, fields, headers, encode_multipart, multipart_boundary, **urlopen_kw)\u001b[0m\n\u001b[1;32m    148\u001b[0m         \u001b[0mextra_kw\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mupdate\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0murlopen_kw\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    149\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 150\u001b[0;31m         \u001b[0;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0murlopen\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mmethod\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0murl\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0mextra_kw\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/urllib3/poolmanager.py\u001b[0m in \u001b[0;36murlopen\u001b[0;34m(self, method, url, redirect, **kw)\u001b[0m\n\u001b[1;32m    322\u001b[0m             \u001b[0mresponse\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mconn\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0murlopen\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mmethod\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0murl\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0mkw\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    323\u001b[0m         \u001b[0;32melse\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 324\u001b[0;31m             \u001b[0mresponse\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mconn\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0murlopen\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mmethod\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mu\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mrequest_uri\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0mkw\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    325\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    326\u001b[0m         \u001b[0mredirect_location\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mredirect\u001b[0m \u001b[0;32mand\u001b[0m \u001b[0mresponse\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mget_redirect_location\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/urllib3/connectionpool.py\u001b[0m in \u001b[0;36murlopen\u001b[0;34m(self, method, url, body, headers, retries, redirect, assert_same_host, timeout, pool_timeout, release_conn, chunked, body_pos, **response_kw)\u001b[0m\n\u001b[1;32m    598\u001b[0m                                                   \u001b[0mtimeout\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mtimeout_obj\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    599\u001b[0m                                                   \u001b[0mbody\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mbody\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mheaders\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mheaders\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 600\u001b[0;31m                                                   chunked=chunked)\n\u001b[0m\u001b[1;32m    601\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    602\u001b[0m             \u001b[0;31m# If we're going to release the connection in ``finally:``, then\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.7/dist-packages/urllib3/connectionpool.py\u001b[0m in \u001b[0;36m_make_request\u001b[0;34m(self, conn, method, url, timeout, chunked, **httplib_request_kw)\u001b[0m\n\u001b[1;32m    378\u001b[0m             \u001b[0;32mexcept\u001b[0m \u001b[0mTypeError\u001b[0m\u001b[0;34m:\u001b[0m  \u001b[0;31m# Python 3\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    379\u001b[0m                 \u001b[0;32mtry\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 380\u001b[0;31m                     \u001b[0mhttplib_response\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mconn\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mgetresponse\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    381\u001b[0m                 \u001b[0;32mexcept\u001b[0m \u001b[0mException\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0me\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    382\u001b[0m                     \u001b[0;31m# Remove the TypeError from the exception chain in Python 3;\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/lib/python3.7/http/client.py\u001b[0m in \u001b[0;36mgetresponse\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m   1367\u001b[0m         \u001b[0;32mtry\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1368\u001b[0m             \u001b[0;32mtry\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 1369\u001b[0;31m                 \u001b[0mresponse\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mbegin\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   1370\u001b[0m             \u001b[0;32mexcept\u001b[0m \u001b[0mConnectionError\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1371\u001b[0m                 \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mclose\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/lib/python3.7/http/client.py\u001b[0m in \u001b[0;36mbegin\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m    308\u001b[0m         \u001b[0;31m# read until we get a non-100 response\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    309\u001b[0m         \u001b[0;32mwhile\u001b[0m \u001b[0;32mTrue\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 310\u001b[0;31m             \u001b[0mversion\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mstatus\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mreason\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_read_status\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    311\u001b[0m             \u001b[0;32mif\u001b[0m \u001b[0mstatus\u001b[0m \u001b[0;34m!=\u001b[0m \u001b[0mCONTINUE\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    312\u001b[0m                 \u001b[0;32mbreak\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/lib/python3.7/http/client.py\u001b[0m in \u001b[0;36m_read_status\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m    269\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    270\u001b[0m     \u001b[0;32mdef\u001b[0m \u001b[0m_read_status\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 271\u001b[0;31m         \u001b[0mline\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mstr\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mfp\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mreadline\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0m_MAXLINE\u001b[0m \u001b[0;34m+\u001b[0m \u001b[0;36m1\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m\"iso-8859-1\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    272\u001b[0m         \u001b[0;32mif\u001b[0m \u001b[0mlen\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mline\u001b[0m\u001b[0;34m)\u001b[0m \u001b[0;34m>\u001b[0m \u001b[0m_MAXLINE\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    273\u001b[0m             \u001b[0;32mraise\u001b[0m \u001b[0mLineTooLong\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"status line\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/lib/python3.7/socket.py\u001b[0m in \u001b[0;36mreadinto\u001b[0;34m(self, b)\u001b[0m\n\u001b[1;32m    587\u001b[0m         \u001b[0;32mwhile\u001b[0m \u001b[0;32mTrue\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    588\u001b[0m             \u001b[0;32mtry\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 589\u001b[0;31m                 \u001b[0;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_sock\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mrecv_into\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mb\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    590\u001b[0m             \u001b[0;32mexcept\u001b[0m \u001b[0mtimeout\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    591\u001b[0m                 \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_timeout_occurred\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;32mTrue\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/lib/python3.7/ssl.py\u001b[0m in \u001b[0;36mrecv_into\u001b[0;34m(self, buffer, nbytes, flags)\u001b[0m\n\u001b[1;32m   1069\u001b[0m                   \u001b[0;34m\"non-zero flags not allowed in calls to recv_into() on %s\"\u001b[0m \u001b[0;34m%\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1070\u001b[0m                   self.__class__)\n\u001b[0;32m-> 1071\u001b[0;31m             \u001b[0;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mread\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mnbytes\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mbuffer\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   1072\u001b[0m         \u001b[0;32melse\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1073\u001b[0m             \u001b[0;32mreturn\u001b[0m \u001b[0msuper\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mrecv_into\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mbuffer\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mnbytes\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mflags\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/lib/python3.7/ssl.py\u001b[0m in \u001b[0;36mread\u001b[0;34m(self, len, buffer)\u001b[0m\n\u001b[1;32m    927\u001b[0m         \u001b[0;32mtry\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    928\u001b[0m             \u001b[0;32mif\u001b[0m \u001b[0mbuffer\u001b[0m \u001b[0;32mis\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 929\u001b[0;31m                 \u001b[0;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_sslobj\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mread\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mlen\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mbuffer\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    930\u001b[0m             \u001b[0;32melse\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    931\u001b[0m                 \u001b[0;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_sslobj\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mread\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mlen\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mKeyboardInterrupt\u001b[0m: "
          ]
        }
      ]
    }
  ]
}
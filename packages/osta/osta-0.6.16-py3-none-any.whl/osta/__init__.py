"""
The osta (OSTolaskujen Analysointi) package offers tools to manipulate and
analyze purchases of Finnish municipalities.

Purchase data of Finnish municipalities has been public information
(Act on the Openness of Government Activities 621/1999). However, the problem
has been accessibility. Association of Finnish Municipalities
(https://www.localfinland.fi/) has recommended that municipalities publish
their purchase data in an easy-accessible format on internet. As a result, a
growing number of municipalities has published their data in opendata.fi
(https://www.avoindata.fi/en) so that everyone has access to it.

The purchase data is published on the website in csv or Excel format.
Despite the guideline of the Association regarding the publishing, at least
older datasets lack of standardization. For example, other municipality might
use other format while others prefer using different format. This means that
datasets between municipalities are not directly compatible with each other.

The osta package aims to resolve the forementioned problem. Below, is an
illustration of a workflow utilizing osta package.

.. image:: figures/osta_workflow.png

There are three modules in the osta package. While wrangle contains generic
methods for data manipulation, import and enrich in importing and enriching
the data, respectively.

The workflow starts by searching and importing the data from opendata.fi
(searchData, getData). Because there are differences in naming formats,
the names of the fields can differ. This means that the type of data in each
column, such as date information or municipality name, must be detected
(detectFields).

After column names are standardized, clean method can be used to standardize
the values of each column. Furthermore, it can be utilized to errors from the
data. After standarzization, multiple datasets can be merged into one with
merge method.

The user can fetch data from different sources. getMuni, getMuniFin,
getMuniComp, getMuniMap, and getComp offer convenient connection to different
databases. The fetched datasets can be then merged to purchase data with
enrich method.

To organize the data to match with the Association's guideline, one can use
organize method. For instance, it can be used to rename the columns and to
remove sensitive data of private people carrying a trade. After the
manipulation step, the data is ready for analysis.

See the osta package demo, that shows how the package can be utilized to
create a purchase data analysis workflow.
(https://github.com/TuomasBorman/osta/blob/main/vignettes/osta.ipynb)

"""

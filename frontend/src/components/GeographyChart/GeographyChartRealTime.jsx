import { useTheme } from "@mui/material";
import { ResponsiveChoropleth } from "@nivo/geo";
import { geoFeatures } from "../../data/geoFeatures";
import { tokens } from "../../theme";
import React, { useState, useEffect } from 'react';

const GeographyChartRealTime = ({ isDashboard = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [data, setData] = useState([])

  useEffect(() => {

    function getGeoRegion(response) {
      return {
        "eastus": "USA",
        "northeurope": "NLD",
        "uksouth": "GBR",
        "westeurope": "IRL",
      }[response.value.location]
    }

    function setCurrentEmissionValues(locations) {
      const promiseCollection = [];
      locations.forEach(location => {
        const apiResult = fetch("http://127.0.0.1:5000/current-emissions?" + new URLSearchParams({
          location: location
        }))
        .then(res => res.json())
        promiseCollection.push(apiResult);
      });

      Promise.all(promiseCollection).then((responses) => {
        setData(responses.map(response => ({
          id: getGeoRegion(response),
          value: 10-response.value.emissions
        })))
      });
    }

    setData([])
    fetch("http://127.0.0.1:5000/locations")
      .then(res => {
        return res.json()
      })
      .then(resources => {
        setCurrentEmissionValues(resources.value)
        setInterval(setCurrentEmissionValues, 1000*30, resources.value)
      })
  }, [])


  return (
    <ResponsiveChoropleth
      data={data}
      theme={{
        axis: {
          domain: {
            line: {
              stroke: colors.grey[100],
            },
          },
          legend: {
            text: {
              fill: colors.grey[100],
            },
          },
          ticks: {
            line: {
              stroke: colors.grey[100],
              strokeWidth: 1,
            },
            text: {
              fill: colors.grey[100],
            },
          },
        },
        legends: {
          text: {
            fill: colors.grey[100],
          },
        },
      }}
      features={geoFeatures.features}
      margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
      colors="RdYlGn"
      domain={[10, 0]}
      unknownColor="#666666"
      label="properties.name"
      valueFormat={(x) => (Math.round((x) * 10) / 10)+'g'}
      projectionType="naturalEarth1"
      projectionScale={200}
      projectionTranslation={[0.5, 0.5]}
      projectionRotation={[0, 0, 0]}
      borderWidth={0.5}
      borderColor="#ffffff"
      isInteractive={true}
      tooltip={function(e){}}
      legends={
        !isDashboard
          ? [
              {
                anchor: "left",
                direction: "column",
                justify: true,
                translateX: 20,
                translateY: 0,
                itemsSpacing: 0,
                itemWidth: 94,
                itemHeight: 18,
                itemDirection: "left-to-right",
                itemTextColor: colors.grey[100],
                itemOpacity: 0.85,
                symbolSize: 18,
                effects: [
                  {
                    on: "hover",
                    style: {
                      itemTextColor: "#ffffff",
                      itemOpacity: 1,
                    },
                  },
                ],
              },
            ]
          : undefined
      }
    />
  );
};

export default GeographyChartRealTime;

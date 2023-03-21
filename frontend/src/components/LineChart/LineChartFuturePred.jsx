import { ResponsiveLine } from "@nivo/line";
import { useTheme } from "@mui/material";
import { tokens } from "../../theme";
import React, { useState, useEffect } from 'react';

const LineChartFuturePred = ({ isCustomLineColors = false, isDashboard = false, resourceGroup="" }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [data, setData] = useState([]);

  useEffect(() => {

    function truncate(str, maxlength) {
      return (str.length > maxlength) ?
        str.slice(0, maxlength - 1) + '…' : str;
    }

    function formatDate(date) {
      console.log(date)
      let res = new Date(date)
        .toLocaleDateString('en-gb', { 
          month:"numeric",
          hour:"numeric",
          day:"numeric",
          minute:"numeric"
        })
        .split(",").join('')
        console.log(res)
        return res
  }

    const setFutureResourceEmissions = (resources) => {
      const promiseCollection = [];
      resources.map(resource => resource.id).forEach(resourceId => {
        const apiResult = fetch("http://127.0.0.1:5000/future-resource-emissions/"+resourceGroup+resourceId)
          .then(res => {
            return res.json()
          })
        promiseCollection.push(apiResult);
      });

      Promise.all(promiseCollection).then((responses) => {
        setData(responses.map((response, i) => {
          return {
            id: truncate(resources[i].name, 21),
            color: tokens("dark").greenAccent[500],
            data: response.value.map(dataPoint => ({
              x: formatDate(dataPoint.date),
              y: dataPoint.value,
            }))
          }
        }))
      });
    }
    
    setData([])
    fetch("http://127.0.0.1:5000/resources/"+resourceGroup)
    .then(res => {
      return res.json()
    })
    .then(resources => {
      setFutureResourceEmissions(resources.value)
    })
  }, [resourceGroup])

  return (
    <ResponsiveLine
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
        tooltip: {
          container: {
            color: colors.primary[500],
          },
        },
      }}
      colors={isDashboard ? { datum: "color" } : { scheme: "nivo" }}
      margin={{ top: 50, right: 180, bottom: 50, left: 60 }}
      xScale={{ 
        format: "%d/%m %H:%M",
        type: "time",
      }}
      xFormat="time:%d/%m %H:%M"
      yScale={{
        type: "linear",
        min: "auto",
        max: "auto",
        stacked: true,
        reverse: false,
      }}
      yFormat=" >-.2f"
      curve="catmullRom"
      axisTop={null}
      axisRight={null}
      axisBottom={{
        orient: "bottom",
        tickSize: 0,
        tickValues: "every day",
        tickPadding: 5,
        tickRotation: 0,
        legend: isDashboard ? undefined : "Time", // added
        legendOffset: 36,
        legendPosition: "middle",
        format: "%d/%m %H:%M",
      }}
      axisLeft={{
        orient: "left",
        tickValues: 5, // added
        tickSize: 3,
        tickPadding: 5,
        tickRotation: 0,
        legend: isDashboard ? undefined : "Carbon Emissions (g)", // added
        legendOffset: -40,
        legendPosition: "middle",
      }}
      enableGridX={false}
      enableGridY={false}
      pointSize={8}
      pointColor={{ theme: "background" }}
      pointBorderWidth={2}
      pointBorderColor={{ from: "serieColor" }}
      pointLabelYOffset={-12}
      useMesh={true}
      legends={[
        {
          anchor: "bottom-right",
          direction: "column",
          justify: false,
          translateX: 100,
          translateY: 0,
          itemsSpacing: 0,
          itemDirection: "left-to-right",
          itemWidth: 80,
          itemHeight: 20,
          itemOpacity: 0.75,
          symbolSize: 12,
          symbolShape: "circle",
          symbolBorderColor: "rgba(0, 0, 0, .5)",
          effects: [
            {
              on: "hover",
              style: {
                itemBackground: "rgba(0, 0, 0, .03)",
                itemOpacity: 1,
              },
            },
          ],
        },
      ]}
    />
  );
};

export default LineChartFuturePred;

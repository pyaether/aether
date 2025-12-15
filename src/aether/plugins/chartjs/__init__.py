from __future__ import (
    annotations,
)  # Remove this when Python 3.12 becomes the minimum supported version.

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ChartJSDataset(BaseModel):
    model_config = ConfigDict(extra="allow")

    label: str
    data: list[Any]
    backgroundColor: str | list[str] | None = None
    borderColor: str | list[str] | None = None
    borderWidth: int = 2
    tension: float | None = None
    fill: bool | None = None
    pointRadius: int | None = None
    pointBackgroundColor: str | list[str] | None = None
    pointBorderColor: str | list[str] | None = None
    hoverBackgroundColor: str | list[str] | None = None
    hoverBorderColor: str | list[str] | None = None
    order: int | None = None
    type: str | None = None  # dataset type override, e.g., 'line', 'bar'
    yAxisID: Literal["y", "y1"] | None = None


class ChartJSData(BaseModel):
    model_config = ConfigDict(extra="allow")

    labels: Annotated[list[str], Field(default_factory=list)]
    datasets: Annotated[list[ChartJSDataset], Field(default_factory=list)]


class ChartJSFont(BaseModel):
    model_config = ConfigDict(extra="allow")

    size: Annotated[int, Field(ge=1)] = 12
    weight: str | None = None
    family: str | None = None
    lineHeight: float | None = None


class ChartJSLegendLabels(BaseModel):
    model_config = ConfigDict(extra="allow")

    usePointStyle: bool = True
    padding: int = 12
    font: Annotated[ChartJSFont, Field(default_factory=ChartJSFont)]
    color: str = "var(--foreground)"


class ChartJSLegend(BaseModel):
    model_config = ConfigDict(extra="allow")

    display: bool = True
    position: Literal["top", "bottom", "left", "right"] = "top"
    labels: Annotated[ChartJSLegendLabels, Field(default_factory=ChartJSLegendLabels)]


class ChartJSTooltip(BaseModel):
    model_config = ConfigDict(extra="allow")

    enabled: bool = True
    mode: str = "index"
    intersect: bool = False
    backgroundColor: str = "var(--background)"
    titleColor: str = "var(--foreground)"
    bodyColor: str = "var(--foreground)"
    borderColor: str = "var(--border)"
    borderWidth: int = 1
    padding: int = 12
    callbacks: dict[str, Any] | None = None  # Allows custom tooltip callbacks


class ChartJSTitle(BaseModel):
    model_config = ConfigDict(extra="allow")

    display: bool = True
    text: str
    padding: int = 20
    font: Annotated[
        ChartJSFont, Field(default_factory=lambda: ChartJSFont(size=16, weight="600"))
    ]
    color: str = "var(--foreground)"


class ChartJSPlugins(BaseModel):
    model_config = ConfigDict(extra="allow")

    legend: Annotated[ChartJSLegend, Field(default_factory=ChartJSLegend)]
    tooltip: Annotated[ChartJSTooltip, Field(default_factory=ChartJSTooltip)]
    title: ChartJSTitle | None = None
    annotation: dict[str, Any] | None = None


class ChartJSAxisGrid(BaseModel):
    model_config = ConfigDict(extra="allow")

    display: bool = True
    color: str = "var(--border) / 0.2"
    drawBorder: bool = False
    drawOnChartArea: bool | None = None


class ChartJSAxisTick(BaseModel):
    model_config = ConfigDict(extra="allow")

    color: str = "var(--muted-foreground)"
    font: Annotated[ChartJSFont, Field(default_factory=ChartJSFont)]


class ChartJSAxis(BaseModel):
    model_config = ConfigDict(extra="allow")

    beginAtZero: bool = True
    grid: Annotated[ChartJSAxisGrid, Field(default_factory=ChartJSAxisGrid)]
    ticks: Annotated[ChartJSAxisTick, Field(default_factory=ChartJSAxisTick)]
    stacked: bool | None = None
    type: str | None = None  # e.g., "linear", "logarithmic", "category", etc.
    min: float | None = None
    max: float | None = None
    position: str | None = None
    display: bool | None = None


class ChartJSScales(BaseModel):
    model_config = ConfigDict(extra="allow")

    x: Annotated[ChartJSAxis, Field(default_factory=ChartJSAxis)]
    y: Annotated[ChartJSAxis, Field(default_factory=ChartJSAxis)]
    x1: Annotated[ChartJSAxis | None, Field(default=None)]
    y1: Annotated[ChartJSAxis | None, Field(default=None)]


class ChartJSOptions(BaseModel):
    model_config = ConfigDict(extra="allow")

    responsive: bool = True
    maintainAspectRatio: bool = False
    plugins: Annotated[ChartJSPlugins, Field(default_factory=ChartJSPlugins)]
    scales: ChartJSScales | None = None
    interaction: dict[str, Any] | None = None
    elements: dict[str, Any] | None = None
    animations: dict[str, Any] | None = None


class ChartJSConfig(BaseModel):
    type: str = "bar"
    data: Annotated[ChartJSData, Field(default_factory=ChartJSData)]
    options: Annotated[ChartJSOptions, Field(default_factory=ChartJSOptions)]


def build_chart_config_from_attributes(
    chart_attributes: dict[str, Any],
) -> ChartJSConfig:
    chart_config = ChartJSConfig()

    if "chart_type" in chart_attributes:
        chart_config.type = chart_attributes["chart_type"]

    if "chart_labels" in chart_attributes:
        chart_config.data.labels = chart_attributes["chart_labels"]

    datasets: list[ChartJSDataset] = []
    if "chart_datasets" in chart_attributes:
        datasets.extend(
            [
                ChartJSDataset(**dataset)
                for dataset in chart_attributes["chart_datasets"]
            ]
        )
    elif "chart_data" in chart_attributes:
        dataset = ChartJSDataset(
            label=chart_attributes.get("chart_label", "Dataset"),
            data=chart_attributes["chart_data"],
            backgroundColor=chart_attributes.get("chart_bg_color", "var(--chart-1)"),
            borderColor=chart_attributes.get("chart_border_color", "var(--chart-1)"),
            borderWidth=chart_attributes.get("chart_border_width", 2),
        )
        if chart_config.type == "line":
            dataset.tension = chart_attributes.get("chart_tension", 0.4)
            dataset.fill = chart_attributes.get("chart_fill", False)
            dataset.pointRadius = chart_attributes.get("chart_point_radius", 3)
        datasets.append(dataset)

    chart_config.data.datasets = datasets

    if "chart_title" in chart_attributes:
        chart_config.options.plugins.title = ChartJSTitle(
            text=chart_attributes["chart_title"]
        )

    if chart_config.type in ["bar", "line", "scatter", "bubble"]:
        scales = ChartJSScales()

        if "chart_scales_x" in chart_attributes:
            scales.x = ChartJSAxis(**chart_attributes["chart_scales_x"])

        if "chart_scales_y" in chart_attributes:
            scales.y = ChartJSAxis(**chart_attributes["chart_scales_y"])

        if chart_config.type in ["line", "scatter"]:
            if "chart_scales_x1" in chart_attributes:
                scales.x1 = ChartJSAxis(**chart_attributes["chart_scales_x1"])

            if "chart_scales_y1" in chart_attributes:
                scales.y1 = ChartJSAxis(**chart_attributes["chart_scales_y1"])

        if chart_attributes.get("chart_stacked"):
            scales.x.stacked = True
            scales.y.stacked = True
        chart_config.options.scales = scales

    return chart_config

"""Interfaces for specific DearPyGui theme color items."""

from dearpygui import dearpygui
from .px_theme import *


__all__ = [
    'Border',
    'BorderShadow',
    'BoxSelector',
    'BoxSelectorOutline',
    'Button',
    'ButtonActive',
    'ButtonHovered',
    'CheckMark',
    'ChildBg',
    'Crosshairs',
    'DockingEmptyBg',
    'DockingPreview',
    'DragDropTarget',
    'ErrorBar',
    'Fill',
    'FrameBg',
    'FrameBgActive',
    'FrameBgHovered',
    'GridBg',
    'GridLine',
    'GridLinePrimary',
    'Header',
    'HeaderActive',
    'HeaderHovered',
    'InlayText',
    'LegendBg',
    'LegendBorder',
    'LegendText',
    'Line',
    'Link',
    'LinkHovered',
    'LinkSelected',
    'MarkerFill',
    'MarkerOutline',
    'MenuBarBg',
    'MiniMapBg',
    'MiniMapBgHovered',
    'MiniMapCanvas',
    'MiniMapCanvasOutline',
    'MiniMapLink',
    'MiniMapLinkSelected',
    'MiniMapNodeBg',
    'MiniMapNodeBgHovered',
    'MiniMapNodeBgSelected',
    'MiniMapNodeOutline',
    'MiniMapOutline',
    'MiniMapOutlineHovered',
    'ModalWindowDimBg',
    'NavHighlight',
    'NavWindowingDimBg',
    'NavWindowingHighlight',
    'NodeBg',
    'NodeBgHovered',
    'NodeBgSelected',
    'NodeOutline',
    'Pin',
    'PinHovered',
    'PlotBg',
    'PlotBorder',
    'PlotHistogram',
    'PlotHistogramHovered',
    'PlotLines',
    'PlotLinesHovered',
    'PopupBg',
    'Query',
    'ResizeGrip',
    'ResizeGripActive',
    'ResizeGripHovered',
    'ScrollbarBg',
    'ScrollbarGrab',
    'ScrollbarGrabActive',
    'ScrollbarGrabHovered',
    'Selection',
    'Separator',
    'SeparatorActive',
    'SeparatorHovered',
    'SliderGrab',
    'SliderGrabActive',
    'Tab',
    'TabActive',
    'TabHovered',
    'TabUnfocused',
    'TabUnfocusedActive',
    'TableBorderLight',
    'TableBorderStrong',
    'TableHeaderBg',
    'TableRowBg',
    'TableRowBgAlt',
    'Text',
    'TextDisabled',
    'TextSelectedBg',
    'TitleBar',
    'TitleBarHovered',
    'TitleBarSelected',
    'TitleBg',
    'TitleBgActive',
    'TitleBgCollapsed',
    'TitleText',
    'WindowBg',
    'XAxis',
    'XAxisGrid',
    'YAxis',
    'YAxis2',
    'YAxis3',
    'YAxisGrid',
    'YAxisGrid2',
    'YAxisGrid3'
]




class Border(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_Border


class BorderShadow(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_BorderShadow


class BoxSelector(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodeCol_BoxSelector


class BoxSelectorOutline(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodeCol_BoxSelectorOutline


class Button(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_Button


class ButtonActive(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_ButtonActive


class ButtonHovered(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_ButtonHovered


class CheckMark(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_CheckMark


class ChildBg(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_ChildBg


class Crosshairs(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_Crosshairs


class DockingEmptyBg(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_DockingEmptyBg


class DockingPreview(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_DockingPreview


class DragDropTarget(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_DragDropTarget


class ErrorBar(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_ErrorBar


class Fill(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_Fill


class FrameBg(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_FrameBg


class FrameBgActive(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_FrameBgActive


class FrameBgHovered(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_FrameBgHovered


class GridBg(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodeCol_GridBackground


class GridLine(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodeCol_GridLine


class GridLinePrimary(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodesCol_GridLinePrimary


class Header(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_Header


class HeaderActive(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_HeaderActive


class HeaderHovered(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_HeaderHovered


class InlayText(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_InlayText


class LegendBg(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_LegendBg


class LegendBorder(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_LegendBorder


class LegendText(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_LegendText


class Line(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_Line


class Link(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodeCol_Link


class LinkHovered(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodeCol_LinkHovered


class LinkSelected(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodeCol_LinkSelected


class MarkerFill(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_MarkerFill


class MarkerOutline(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_MarkerOutline


class MenuBarBg(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_MenuBarBg


class MiniMapBg(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodesCol_MiniMapBackground


class MiniMapBgHovered(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodesCol_MiniMapBackgroundHovered


class MiniMapCanvas(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodesCol_MiniMapCanvas


class MiniMapCanvasOutline(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodesCol_MiniMapCanvasOutline


class MiniMapLink(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodesCol_MiniMapLink


class MiniMapLinkSelected(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodesCol_MiniMapLinkSelected


class MiniMapNodeBg(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodesCol_MiniMapNodeBackground


class MiniMapNodeBgHovered(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodesCol_MiniMapNodeBackgroundHovered


class MiniMapNodeBgSelected(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodesCol_MiniMapNodeBackgroundSelected


class MiniMapNodeOutline(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodesCol_MiniMapNodeOutline


class MiniMapOutline(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodesCol_MiniMapOutline


class MiniMapOutlineHovered(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodesCol_MiniMapOutlineHovered


class ModalWindowDimBg(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_ModalWindowDimBg


class NavHighlight(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_NavHighlight


class NavWindowingDimBg(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_NavWindowingDimBg


class NavWindowingHighlight(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_NavWindowingHighlight


class NodeBg(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodeCol_NodeBackground


class NodeBgHovered(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodeCol_NodeBackgroundHovered


class NodeBgSelected(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodeCol_NodeBackgroundSelected


class NodeOutline(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodeCol_NodeOutline


class Pin(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodeCol_Pin


class PinHovered(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodeCol_PinHovered


class PlotBg(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_PlotBg


class PlotBorder(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_PlotBorder


class PlotHistogram(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_PlotHistogram


class PlotHistogramHovered(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_PlotHistogramHovered


class PlotLines(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_PlotLines


class PlotLinesHovered(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_PlotLinesHovered


class PopupBg(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_PopupBg


class Query(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_Query


class ResizeGrip(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_ResizeGrip


class ResizeGripActive(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_ResizeGripActive


class ResizeGripHovered(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_ResizeGripHovered


class ScrollbarBg(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_ScrollbarBg


class ScrollbarGrab(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_ScrollbarGrab


class ScrollbarGrabActive(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_ScrollbarGrabActive


class ScrollbarGrabHovered(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_ScrollbarGrabHovered


class Selection(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_Selection


class Separator(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_Separator


class SeparatorActive(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_SeparatorActive


class SeparatorHovered(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_SeparatorHovered


class SliderGrab(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_SliderGrab


class SliderGrabActive(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_SliderGrabActive


class Tab(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_Tab


class TabActive(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_TabActive


class TabHovered(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_TabHovered


class TabUnfocused(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_TabUnfocused


class TabUnfocusedActive(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_TabUnfocusedActive


class TableBorderLight(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_TableBorderLight


class TableBorderStrong(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_TableBorderStrong


class TableHeaderBg(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_TableHeaderBg


class TableRowBg(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_TableRowBg


class TableRowBgAlt(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_TableRowBgAlt


class Text(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_Text


class TextDisabled(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_TextDisabled


class TextSelectedBg(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_TextSelectedBg


class TitleBar(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodeCol_TitleBar


class TitleBarHovered(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodeCol_TitleBarHovered


class TitleBarSelected(pxThemeColor, ThemeCatNode):
    target = dearpygui.mvNodeCol_TitleBarSelected


class TitleBg(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_TitleBg


class TitleBgActive(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_TitleBgActive


class TitleBgCollapsed(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_TitleBgCollapsed


class TitleText(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_TitleText


class WindowBg(pxThemeColor, ThemeCatCore):
    target = dearpygui.mvThemeCol_WindowBg


class XAxis(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_XAxis


class XAxisGrid(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_XAxisGrid


class YAxis(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_YAxis


class YAxis2(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_YAxis2


class YAxis3(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_YAxis3


class YAxisGrid(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_YAxisGrid


class YAxisGrid2(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_YAxisGrid2


class YAxisGrid3(pxThemeColor, ThemeCatPlot):
    target = dearpygui.mvPlotCol_YAxisGrid3



<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "villages" %>
<%block name="title">${_('Languages')}</%block>

<h2>Mapping Dogon villages</h2>
<p>
    We have been mapping villages in the Dogon and montane Songhay (Hombori, Kikara) areas, and have
    included neighboring or interspersed non-Dogon (e.g. Fulbe, Bozo) villages, beginning in early 2011,
    in collaboration with the LLMAP project. For each village, we ideally collect the following
    information: official name, name in local language(s) in transcription, GPS coordinates, topography
    (sandy plains, base of cliffs, plateau), predominant family (i.e. clan) name, and anything else
    notable about the village (e.g. "known for healers of broken bones"). Typically we take one or two
    photographs to show the terrain the village is in. We assign each village a five-digit code number.
</p>
<p>
    We have visited several hundred villages in the area. For those that we have not yet visited, we try
    to estimate coordinates from maps. However, the only detailed maps available are those inherited from
    the colonial period (but still printed up and sold at the Institut de Géographie in Bamako). These
    old maps have some inaccuracies and anachronisms, as when an entire village has relocated from the
    plateau onto the base of the nearby cliffs or onto the plains. Regarding topography, many large areas
    marked as "forests" in the old maps are now sandy plain (lightly wooded at best).
</p>
<p>
    In addition to visiting the remaining Dogon villages for the LLMAP collaboration, we plan to develop
    additional customized maps for our own site and for use in the field. For example, we will develop map
    schemas including Dogon-internal language boundaries that can be used flexibly to display isogloss
    distributions for lexical and grammatical data.
</p>
<p>
    As the primary in-field mapping winds down, we will turn our attention to working out the historical
    relationships among the villages. Oral history can accurately capture population movements in relatively
    recent times (relocations and splits or mergers of villages, founding of new villages). At deeper time
    depths, oral history morphs into stories of Mande origins. Eventually our mappings and oral histories
    will need to be triangulated with the results of human biological and archeological study.
</p>

${request.map.render()}

${ctx.render()}

---
language:
- en
pretty_name: HSSD
tags:
- 3D scenes
- Embodied AI
license: cc-by-nc-4.0
extra_gated_heading: "Acknowledge license to accept the repository"
extra_gated_prompt: "You agree to use this dataset under the [CC BY-NC 4.0 license](https://creativecommons.org/licenses/by-nc/4.0/) terms"
viewer: false
---

HSSD: Habitat Synthetic Scenes Dataset
==================================

The [Habitat Synthetic Scenes Dataset (HSSD)](https://3dlg-hcvc.github.io/hssd/) is a human-authored 3D scene dataset that more closely mirrors real scenes than prior datasets.
Our dataset represents real interiors and contains a diverse set of 211 scenes and more than 18000 models of real-world objects.

<img src="https://i.imgur.com/XEkLxNs.png" width=50%>

This repository provides a Habitat consumption-ready compressed version of HSSD.
See [this repository](https://huggingface.co/datasets/hssd/hssd-models) for corresponding uncompressed assets.

## Dataset Structure

```
├── objects
│   ├── */*.glb
│   ├── */*.collider.glb
│   ├── */*.filteredSupportSurface(.ply|.glb)
│   ├── */*.object_config.json
├── stages
│   ├── *.glb
│   ├── *.stage_config.json
├── scenes
│   ├── *.scene_instance.json
├── scenes_uncluttered
│   ├── *.scene_instance.json
├── scenes_articulated
│   ├── *.scene_instance.json
├── scene_filter_files
│   ├── *.rec_filter.json
├── metadata
│   ├── *.csv
│   ├── *.json
├── semantics
│   ├── hssd-hab_semantic_lexicon.json
│   ├── scenes
|      ├── *.semantic_config.json
├── urdf
│   ├── <model_name>
|      ├── *.glb
|      ├── *.urdf
|      ├── *.ao_config.json
└── hssd-hab.scene_dataset_config.json
└── hssd-hab-uncluttered.scene_dataset_config.json
└── hssd-hab-articulated.scene_dataset_config.json
```

- `hssd-hab.scene_dataset_config.json`: This SceneDataset config file aggregates the assets and metadata necessary to fully describe the set of stages, objects, and scenes constituting the dataset.
- `objects`: 3D models representing distinct objects that are used to compose scenes. Contains configuration files, render assets, collider assets, and Receptacle mesh assets.
- `stages`: A stage in Habitat is the set of static mesh components which make up the backdrop of a scene (e.g. floor, walls, stairs, etc.).
- `scenes`: A scene is a single 3D world composed of a static stage and a variable number of objects.
- `scene_filter_files`: These .rec_filter.json files contain mappings of Receptacle instance unique_names to active or filtered sets based on their locations and accessibility within the scene. They also contain a "within_set" defining Receptacles which can only be accessed when the parent Furniture object's "default_link" is in the "open" state.
- `metadata`: The metadata directory contains several csv and json files which provide semantic mappings for objects in the dataset as well as rational mappings from regions to the types of clutter objects typically found in them to support procedural generation.
- `semantics`: Primarily defines instance semantics for the scenes. *.semantic_config.json files contain the region annotations for each scene.
- `urdf`: The urdf directory contains the articulated furniture assets, each contained in its own sub-directory named after the source asset. The .urdf files define the articulation properties. Each .glb file is either a render asset or Receptacle mesh connected to a rigid link. The .ao_config.json file contains habitat-specific metadata such as markersets and Receptacle definitions.

### Rearrange-ready assets:
Supporting Habitat 3.0 embodied rearrangement tasks with updated colliders, adjusted and de-cluttered scene contents, receptacle meshes, and receptacle filter files. See [aihabitat.org/habitat3/](aihabitat.org/habitat3/) for more details.
- `hssd-hab-uncluttered.scene_dataset_config.json`: This SceneDataset config file aggregates adds the adjusted and uncluttered scenes for rearrangement tasks.
- `scenes_uncluttered`: Contains the adjusted scene instance configuration files.
- `scene_filter_files`: A scene filter file organizes available Receptacle instances in a scene into active and inactive groups based on simualtion heuristics and manual edits. It is consumed by the RearrangeEpisodeGenerator to construct valid RearrangeEpisodeDatasets.

### Articulated scenes and assets:
Introduced in `v0.3.0`, the `hssd-hab-articulated.scene_dataset_config.json` SceneDataset provides 202 fully articulated HSSD scenes ready for use within the AI Habitat simulation ecosystem. Note that only 161 are publicly available on this repo. The remainder and their unique assets are reserved as an internal test set.

To enable more realistic indoor object manipulation, articulated 3D furniture models such as drawers, cabinets, and appliances were added to replace rigid assets. These models were converted from rigid source assets in HSSD and swapped into the scenes.

Furniture is annotated with a set of Receptacles (surfaces which support small object placement such as shelves and drawers) and can be opened and closed by the agents. Receptacles are further filtered contextually in each scene to ensure that the active set is accessible to the agents.

Additional annotations include point or marker sets for each furniture, region annotations, and semantic classification of objects.

## Getting Started

To load HSSD scenes into the Habitat simulator, you can start by installing [habitat-sim](https://github.com/facebookresearch/habitat-sim) using instructions specified [here](https://github.com/facebookresearch/habitat-sim#installation).

Once installed, you can run the interactive Habitat viewer to load a scene:

```
habitat-viewer --dataset /path/to/hssd-hab/hssd-hab.scene_dataset_config.json -- 102344280
# or ./build/viewer if compiling from source
```

You can find more information about using the interactive viewer [here](https://github.com/facebookresearch/habitat-sim#testing:~:text=path/to/data/-,Interactive%20testing,-%3A%20Use%20the%20interactive).

Habitat-Sim is typically used with [Habitat-Lab](https://github.com/facebookresearch/habitat-lab), a modular high-level library for end-to-end experiments in embodied AI.
To define embodied AI tasks (e.g. navigation, instruction following, question answering), train agents, and benchmark their performance using standard metrics, you can download habitat-lab using the instructions provided [here](https://github.com/facebookresearch/habitat-lab#installation).

## Changelog
- `v0.3.0`: **Articulated Scenes and PARTNR support**
   - This major version update adds a large set of changes to support the introduction of 202 articulated HSSD scenes and the [PARTNR benchmark](https://github.com/facebookresearch/partnr-planner).
   - Includes improvements to stage texture/geometry and object collision shapes and receptacles.
   - Adds:
      -  2000+ articulated assets in the urdf/ directory representing and replacing rigid furniture objects. Annotated with Receptacles and semantics.
      - 202 new articulated scenes with rigid objects replaced by AOs. These are uncluttered and often significantly altered from originals to accommodate the new assets.
        - Note that test scenes and assets are removed before migration to this repo.
      - Receptacle filter files for new scenes annotating accessible Receptacles and "within" Receptacles (those which require opening an articulated link for access).
         - Note that only one link per AO is configured with an active Receptacle. This is based on logic in PARTNR and habitat-lab (default_link).
      - Region volume semantic annotations to all scenes
      - Semantic lexicon file with updated classes
      - Metadata files mapping object semantics and common-sense object->region sets for PARTNR
 - `v0.2.5`: **Rearrange-ready HSSD**
   - Note: this is a checkpoint. Known issues exist and continued polish is ongoing.
   - Adds Receptacle meshes describing support surfaces for small objects (e.g. table or shelf surfaces).
   - Adds collider meshes (.collider.glb) for assets with Receptacle meshes to support simulation.
   - Adds new scenes 'scenes_uncluttered' and new SceneDataset 'hssd-hab-uncluttered' containing adjusted and de-cluttered versions of the scenes for use in embodied rearrangement tasks.
   - Adds 'scene_filter_files' which sort Receptacles in each scene into active and inactive groups for RearrangeEpisode generation.
 - `v0.2.4`: 
   - Recompresses several object GLBs to preserve PBR material status. 
   - Adds CSV with object metadata and semantic lexicon files for Habitat.
   - Adds train/val scene splits file.
- `v0.2.3`: First release.


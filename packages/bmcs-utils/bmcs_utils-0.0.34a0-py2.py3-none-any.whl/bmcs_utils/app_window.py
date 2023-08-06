'''
Application Window for as a user interface to implemented models within Jupyter

 - The AppWindow class can generate a user interface to a model.
   It generates the interface based on the specified views and handlers
   provided by the model.

'''

import ipywidgets as ipw
import ipytree as ipt
import traits.api as tr
from .tree_node import BMCSNode
from bmcs_utils.i_model import IModel
import bmcs_utils.config as config
print_output = ipw.Output(layout=ipw.Layout(width="100%"))

class AppWindow(tr.HasTraits):
    '''Container class synchronizing the interactionjup elements with plotting area.
    It is equivalent to the traitsui.View class
    '''
    model = tr.Instance(IModel)

    figsize = tr.Tuple(8, 3)

    def __init__(self, model, **kw):
        super(AppWindow, self).__init__(**kw)
        self.model = model
        self.output = ipw.Output()

    plot_backend_table = tr.Dict
    def _plot_backend_table_default(self):
        return {key : config.available_plot_backends[key]() for key
                in config.active_plot_backends}

    # Shared layouts -
    left_pane_layout = tr.Instance(ipw.Layout)
    def _left_pane_layout_default(self):
        return ipw.Layout(
            #border='solid 1px black',
            margin='0px 0px 0px 0px',
            padding='0px 0px 0px 0px',
            width="300px",
            flex_grow="1",
        )

    right_pane_layout = tr.Instance(ipw.Layout)
    def _right_pane_layout_default(self):
        return ipw.Layout(
            border='solid 1px black',
            margin='0px 0px 0px 5px',
            padding='1px 1px 1px 1px',
            width="100%",
            flex_grow="1",
        )

    def interact(self):
        left_pane = ipw.VBox([self.tree_pane, self.model_editor_pane],
                             layout=self.left_pane_layout)
        name = self.model.name
        self.menubar = ipw.Label(value=name, layout=ipw.Layout(width="100%", height="150px"))
        self.empty_pane = ipw.Box(layout=ipw.Layout(width="100%", height="100%"))
        self.plot_pane = ipw.VBox([self.menubar, self.empty_pane],
                       layout=ipw.Layout(align_items="stretch",
                                         #border='solid 1px black',
                                         width="100%"))
        right_pane = ipw.VBox([self.plot_pane, self.time_editor_pane],
                               layout=self.right_pane_layout)
        app = ipw.HBox([left_pane, right_pane],
                        layout=ipw.Layout(align_items="stretch",
                                          width="100%"))
        app_print = ipw.VBox([app, print_output],
                             layout=ipw.Layout(align_items="stretch",
                                               width="100%"))
        self.model_tree.selected = True
        display(app_print)

    model_tree = tr.Property(depends_on='model.graph_changed')
    @tr.cached_property
    def _get_model_tree(self):
        tree = self.model.get_tree_subnode(self.model.name)
        return self.get_tree_entries(tree)

    def get_tree_entries(self, tree):
        name, model, subnodes = tree
        bmcs_subnodes = [
            self.get_tree_entries(subnode) for subnode in subnodes
        ]
        node_ = BMCSNode(name, nodes=tuple(bmcs_subnodes),
                         controller=model.get_controller(self))
        node_.observe(self.select_node, 'selected')
        def update_node(event):
            '''upon tree change - rebuild the subnodes'''
            #new_node = model.get_tree_subnode(model.name)
            new_node = model.get_tree_subnode(name)
            new_node_ = self.get_tree_entries(new_node)
            node_.nodes = new_node_.nodes
            # are the original nodes deleted? memory leak?
            # are the original observers deleted?
            # this has been
        model.observe(update_node, 'graph_changed')
        return node_

    tree_pane = tr.Property # might depend on the model
    @tr.cached_property
    def _get_tree_pane(self):
        # provide a method scanning the tree of the model
        # components
        tree_layout = ipw.Layout(display='flex',
                                 overflow_y='scroll',
                                 overflow_x='scroll',
                                 flex_flow='column',
                                 border='solid 1px black',
                                 margin='0px 5px 5px 0px',
                                 padding='1px 1px 15px 1px',
                                 align_items='stretch',
                                 flex_grow="2",
                                 height="30%",
                                 width='100%')

        tree_pane = ipt.Tree(layout=tree_layout)
        root_node = self.model_tree
        tree_pane.nodes = (root_node,)
        return tree_pane

    model_editor_pane = tr.Property # should depend on the model
    @tr.cached_property
    def _get_model_editor_pane(self):
        editor_pane_layout = ipw.Layout(
            display='flex',
            border='solid 1px black',
            overflow='scroll hidden',
            justify_content='space-between',
            flex_flow='column',
            padding='10px 5px 10px 5px',
            margin='0px 5px 0px 0px',
            align_items='flex-start',
            height="70%",
            width='100%')
        return ipw.VBox(layout=editor_pane_layout)

    time_editor_pane_layout = tr.Instance(ipw.Layout)
    def _time_editor_pane_layout_default(self):
        return ipw.Layout(
            height="35px", width="100%",
            margin='0px 0px 0px 0px',
            padding='0px 0px 0px 0px',
        )

    time_editor_pane = tr.Property # should depend on the model
    @tr.cached_property
    def _get_time_editor_pane(self):
        return ipw.VBox(layout=self.time_editor_pane_layout)

    def select_node(self, event):
        if event['old']:
            return
        node = event['owner']
        controller = node.controller
        self.controller = controller
        time_editor = controller.time_editor
        self.time_editor_pane.children = time_editor
        self.controller.update_time_editor()

        # trait = node.trait
        # trait_type = trait.trait_type
        # editor_factory = trait_type.editor_factory
        # if editor_factory:
        #     editor = editor_factory()
        #     print('tt', trait_type)
        #     print('editor', editor)

        model_editor = controller.model_editor
        self.model_editor_pane.children = model_editor.children
        backend = controller.model.plot_backend
        self.set_plot_backend(backend)
        self.setup_plot(controller.model)
        self.update_plot(controller.model)

    current_plot_backend = tr.Str

    pb = tr.Property()
    def _get_pb(self):
        '''Get the current plot backend'''
        return self.plot_backend_table[self.current_plot_backend]

    def set_plot_backend(self, backend):
        if self.current_plot_backend == backend:
            return
        self.current_plot_backend = backend
        pb = self.plot_backend_table[backend]
        self.plot_pane.children = [pb.plot_widget]

    def setup_plot(self, model):
        # TODO: This is being called each time when a model tap in the tree is clicked (node clicked),
        #  is that the desired behaviour?
        pb = self.plot_backend_table[self.current_plot_backend]
        pb.clear_fig()
        pb.setup_plot(model)

    def update_plot(self, model):
        pb = self.plot_backend_table[self.current_plot_backend]
        pb.update_plot(model)
        pb.show_fig()


# backward compatibility
InteractiveWindow = AppWindow
from borneo import ListTablesRequest, GetTableRequest, DeleteRequest, GetRequest, PutRequest, QueryRequest, TableLimits, TableRequest
import traceback
from parameters import file_path, table_name1, table_name2, R, step
from handle import get_handle
import shapefile
import numpy as np
import matplotlib.pyplot as plt
from VertexCoordinates import find_vertex_coordinates, sectors, vertex_belonging_sector, one_sector


def main():
    handle = None

    sf = shapefile.Reader(file_path)
    shapes = sf.shapes()
    coordinates = list(shapes[0].points)
    parts = shapes[0].parts

    coordinates = coordinates[parts[-2]:parts[-1]]
    coordinates = np.array(coordinates)
    koef_x = float(1316 / (coordinates[:, 0].max() - coordinates[:, 0].min()))
    koef_y = float(893 / (coordinates[:, 1].max() - coordinates[:, 1].min()))
    coordinates[:, 0] = coordinates[:, 0] * koef_x
    coordinates[:, 1] = coordinates[:, 1] * koef_y

    fig, ax = plt.subplots()
    ax.plot(coordinates[:, 0], coordinates[:, 1])
    ax.set(title='Ukraine')

    # try:
    #     handle = get_handle()
    #
    #     print("Create table UkraineCooordinates")
    #     statement = 'Create table if not exists ' + table_name1 + '(id integer, X double, Y double, primary key(id))'
    #     request = TableRequest().set_statement(statement)
    #     handle.do_table_request(request, 50000, 3000)
    #
    #     request = PutRequest().set_table_name(table_name1)
    #     for i in range(coordinates.shape[0]):
    #         value = {'id': i, 'x': coordinates[i, 0], 'y': coordinates[i, 1]}
    #         request.set_value(value)
    #         handle.put(request)
    #
    # except Exception as e:
    #     print(e)
    #     traceback.print_exc()
    # finally:
    #     # If the handle isn't closed Python will not exit properly
    #     if handle is not None:
    #         handle.close()

    vertex_coordinates_x, vertex_coordinates_y = find_vertex_coordinates(coordinates)
    ax.scatter(vertex_coordinates_x, vertex_coordinates_y, s=20, c='red')

    # try:
    #     handle = get_handle()
    #     print("Create table VertexCoordinate")
    #     statement = 'Create table if not exists ' + table_name2 + '(id integer, X double, Y double, primary key(id))'
    #     request = TableRequest().set_statement(statement)
    #     handle.do_table_request(request, 50000, 3000)
    #
    #     request = PutRequest().set_table_name(table_name2)
    #     for i in range(len(pX)):
    #         value = {'id': i, 'x': vertex_coordinates_x[i], 'y': vertex_coordinates_y[i]}
    #         request.set_value(value)
    #         handle.put(request)
    # except Exception as e:
    #     print(e)
    #     traceback.print_exc()
    # finally:
    #     # If the handle isn't closed Python will not exit properly
    #     if handle is not None:
    #         handle.close()
    #
    # sector_x, sector_y = sectors(vertex_coordinates_x, vertex_coordinates_y)
    # for i in range(0, len(sector_x), 2):
    #     ax.plot(sector_x[i:i + 2], sector_y[i:i + 2], color='y')

    sector_x, sector_y = one_sector(vertex_coordinates_x[100], vertex_coordinates_y[100])
    for i in range(0, len(sector_x), 2):
        ax.plot(sector_x[i:i+2], sector_y[i:i+2], color='y')
    circle = plt.Circle((vertex_coordinates_x[100], vertex_coordinates_y[100]), R, color='y', fill=False)
    ax.add_artist(circle)
    sector1, sector2, sector3 = vertex_belonging_sector(vertex_coordinates_x[100], vertex_coordinates_y[100], vertex_coordinates_x, vertex_coordinates_y)
    ax.scatter(sector1[:, 0], sector1[:, 1], s=20, color='green')
    ax.scatter(sector2[:, 0], sector2[:, 1], s=20, color='black')
    ax.scatter(sector3[:, 0], sector3[:, 1], s=20, color='purple')
    plt.show()


if __name__ == '__main__':
    main()

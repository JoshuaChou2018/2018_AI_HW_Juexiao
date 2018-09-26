class Node:
    def __int__(self):
        self.unable = False
        self.distanceFromDes = -1  # 距离终点的距离
        self.distanceFromOri = -1  # 距离起点的距离
        self.allDistance = -1
        self.added = False
        self.closed = False
        self.parent = None
        self.x = -1
        self.y = -1


def GenerateMap(m, n):
    map = list()
    for j in range(m):
        nodeRow = list()
        map.append(nodeRow)
        for i in range(n):
            node = Node()
            node.y = j
            node.x = i
            node.unable = False
            node.distanceFromDes = -1  # 距离终点的距离
            node.distanceFromOri = -1  # 距离起点的距离
            node.allDistance = -1
            node.added = False
            node.closed = False
            node.parent = None
            nodeRow.append(node)
    return map


def SetUnableMapNode(map, ls=()):  # 要求一个坐标队列，里边的点上的Node的unable == True
    for index in ls:
        map[index[0]][index[1]].unable = True
    return map


def GetDistanceFromDes(map, mapSize, desIndex):  # map二维数组，mapsize(m,n),desIndex终点坐标
    for ls in map:
        for node in ls:
            node.added = False
    desNode = map[desIndex[0]][desIndex[1]]
    desNode.distanceFromDes = 0
    addedList = list()  # 已经加入的队列，已有值distanceFromDes
    needList = list()  # 待加入的队列，需要评估值distanceFromDes
    addedList.append(desNode)
    desNode.added = True
    while (len(addedList) != 0):  # 当地图上所有可以遍历的点还没全确定
        while (len(addedList) != 0):  # 当一个大循环中，addedList还没被needList取代
            # 从addedList中选出来的一个点，找needList中的needNode
            mainNode = addedList.pop(0)
            mainDistanceFromDes = mainNode.distanceFromDes
            y = mainNode.y
            x = mainNode.x
            for needNodey in (y + 1, y, y - 1):
                if needNodey < 0 or needNodey >= mapSize[0]:
                    continue
                for needNodex in (x + 1, x, x - 1):
                    if needNodex < 0 or needNodex >= mapSize[1]:
                        continue
                    needNode = map[needNodey][needNodex]  # 坐标不出界
                    if needNode.unable == True or needNode.added == True:
                        continue  # 坐标也满足add的要求
                    yOffset = needNodey - y
                    xOffset = needNodex - x
                    allOffset = yOffset + xOffset
                    if allOffset == 1 or allOffset == -1:
                        distanceFromDes = mainDistanceFromDes + 1
                    elif allOffset == -2 or allOffset == 0 or allOffset == 2:
                        distanceFromDes = mainDistanceFromDes + 1.4
                    else:
                        print("error in needNode's distanceFromDes")

                    if needNode in needList:  # 设置needNode的距离，要求最小
                        if distanceFromDes < needNode.distanceFromDes:
                            needNode.distanceFromDes = distanceFromDes
                    else:  # needNode 不在needList中 distanceFromDes一定是-1
                        needNode.distanceFromDes = distanceFromDes
                        needList.append(needNode)
                    # print(needNode.y,needNode.x,needNode.distanceFromDes)
        # needList 已满 addedList已空
        addedList = needList
        for node in addedList:
            node.added = True
        needList = list()
    return map


def GetMinDistanceNodeList(map, mapSize, oriIndex, desIndex):
    for ls in map:
        for node in ls:
            node.added = False
    openedList = list()
    node = map[oriIndex[0]][oriIndex[1]]
    node.distanceFromOri = 0
    node.allDistance = 0
    openedList.append(node)
    node.added = True
    while len(openedList) != 0:
        # print('new turn')
        node = openedList.pop(0)
        node.closed = True
        if node.x == desIndex[0] and node.y == desIndex[1]:
            finalListNeedReverse = list()
            while node != None:
                finalListNeedReverse.append(node)
                node = node.parent
            finalListNeedReverse.reverse()
            return finalListNeedReverse
        neighboursList = list()
        y = node.y
        x = node.x
        parentDistanceFromOri = node.distanceFromOri
        for needNodey in (y + 1, y, y - 1):
            if needNodey < 0 or needNodey >= mapSize[0]:
                continue
            for needNodex in (x + 1, x, x - 1):
                if needNodex < 0 or needNodex >= mapSize[1]:
                    continue
                needNode = map[needNodey][needNodex]  # 坐标不出界
                if needNode.unable == True or needNode.closed == True or needNode.added == True:
                    continue  # 坐标也满足add的要求
                yOffset = needNodey - y
                xOffset = needNodex - x
                allOffset = yOffset + xOffset
                if allOffset == 1 or allOffset == -1:
                    distanceFromOri = parentDistanceFromOri + 1
                elif allOffset == -2 or allOffset == 0 or allOffset == 2:
                    distanceFromOri = parentDistanceFromOri + 1.4
                else:
                    print("error in needNode's distanceFromDes")
                if needNode in neighboursList:  # 设置needNode的距离，要求最小
                    if distanceFromOri < needNode.distanceFromOri:
                        needNode.distanceFromOri = distanceFromOri
                else:  # needNode 不在needList中 distanceFromDes一定是-1
                    needNode.distanceFromOri = distanceFromOri
                    neighboursList.append(needNode)  # 距离计算完成
        for needNode in neighboursList:  # 开始添加至openedList
            needNode.parent = node
            needNode.allDistance = needNode.distanceFromOri + needNode.distanceFromDes
            needNode.added = True
            openedList.append(needNode)
            # print(needNode.x,needNode.y,needNode.allDistance)
        openedList.sort(key=lambda x: x.allDistance)  # 最小距离的排在前边
    print("Cant find any way to the destination!")
    return None


def main():
    TestGetDistanceFromDes()


def TestGetDistanceFromDes():
    m = 27  # 设置地图的长
    n = 25  # 设置地图的宽
    oriIndex = (0, 0)  # 设置起点坐标
    desIndex = (23, 24)  # 设置终点坐标
    map = GenerateMap(m, n)  # 生成地图节点
    obstacleList = [(1, 1), (2, 1), (3, 1), (4, 3), (1, 3), (2, 3), (3, 3), (0, 1), (5, 1), (5, 3)]  # 设置障碍
    map = SetUnableMapNode(map, obstacleList)  # 在地图中添加障碍
    GetDistanceFromDes(map, (m, n), desIndex)  # 添加终点，并计算节点与终点的距离

    print("Distance From Destination")
    for nodeRow in map:
        for node in nodeRow:
            if node.distanceFromDes != -1:
                print('{:^5.1f}'.format(node.distanceFromDes), end=" ")
            else:
                print('  X  ', end=" ")
        print()
    print()

    TestGetMinDistanceNodeList(map, (m, n), oriIndex, desIndex)  # 终点距离测试完了，进入下一阶段


def TestGetMinDistanceNodeList(map, mapSize, oriIndex, desIndex):
    finalList = GetMinDistanceNodeList(map, mapSize, oriIndex, desIndex)  # 添加起点，并生成起点到终点的节点队列

    directions = (('↘', '↓', '↙'), ('→', "S", '←'), ('↗', '↑', '↖'))
    print('How To Go')
    for nodeRow in map:
        for node in nodeRow:
            if node in finalList:
                # print('  *  ',end ='')
                parent = node.parent
                if parent != None:
                    if node.y != desIndex[0] or node.x != desIndex[1]:
                        (y, x) = (parent.y - node.y + 1, parent.x - node.x + 1)
                        print('  ' + directions[y][x] + '  ', end='')
                    else:
                        print('Final', end='')
                else:
                    print('Start', end='')
            else:
                if node.allDistance != -1:
                    print('{:^4.1f}'.format(node.allDistance), end=" ")
                else:
                    print('  X  ', end=" ")
        print()
    print()


main()

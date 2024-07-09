# opengl绘制点的过程：
所有资料都可以从docs.gl查到
opengl是个状态机

#### 1.创建缓冲区，并绑定缓冲区
#### 2.为缓冲区指定数据
#### 3.设置顶点属性，启动顶点属性布局
只要绑定了缓冲区，就可以设置定点属性，不需要看2是否完成
启用顶点属性布局：glEnableVertexAttribArray(mVertexAttribPos);
设置顶点属性：glVertexAttribPointer(index,每个点有几个属性,属性类型,是否正则化,stride步长,pointer)
#### 4.向缓冲区发送绘制指令
有两种方法：
k代表点的数量
(1) glDrawArrays(GL_TRIANGLES, 0, k)
(2) glDrawElements(GL_TRIANGLES, k, GL_UNSIGNED_INT, (void *) 0)
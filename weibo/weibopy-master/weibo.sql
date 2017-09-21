/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     12/16/2014 2:44:37 PM                        */
/*==============================================================*/

create database weibo DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

use weibo;

drop table if exists comments;

drop table if exists geo;

drop table if exists status;

drop table if exists users;

/*==============================================================*/
/* Table: comments                                              */
/*==============================================================*/
create table comments
(
   cid                  bigint not null,
   sid                  bigint not null,
   userid               bigint not null,
   reply2Id             bigint,
   mid_num              bigint,
   idstr                varchar(64),
   ctext                text not null comment '评论内容',
   csource              varchar(256) comment '评论来源',
   create_at            varchar(64) not null comment '创建时间',
   primary key (cid)
);

/*==============================================================*/
/* Table: geo                                                   */
/*==============================================================*/
create table geo
(
   gid                  int not null auto_increment,
   longitude            varchar(16),
   latitude             varchar(16),
   city                 varchar(8) not null,
   province             varchar(8) not null,
   city_name            varchar(16) not null,
   province_name        varchar(8) not null,
   address              varchar(128),
   address_pinyin       varchar(256),
   more                 text,
   primary key (gid),
   key AK_gid (longitude, latitude)
);

/*==============================================================*/
/* Table: status                                                */
/*==============================================================*/
create table status
(
   sid                  bigint not null,
   userid               bigint,
   retweetOfId          bigint,
   gid                  int,
   mid_num              bigint,
   idstr                varchar(64),
   text                 text not null comment '微博信息内容',
   source               varchar(256) comment '微博来源',
   create_at            varchar(64) not null comment '创建时间',
   reposts_count        int not null default 0 comment '转发数',
   comments_count       int not null default 0 comment '评论数',
   attitude_count       int not null default 0 comment '表态数',
   favorited            bool default 0 comment '是否已被收藏',
   truncated            bool default 0 comment '是否被截断',
   bmiddle_pic		varchar(256),
   primary key (sid)
);

/*==============================================================*/
/* Table: users                                                 */
/*==============================================================*/
create table users
(
   userid               bigint not null,
   idstr                varchar(64),
   screen_name          varchar(32) not null comment '用户昵称',
   name                 varchar(32) comment '友好显示名称',
   province             varchar(8),
   city                 varchar(8),
   location             varchar(128) comment '用户所在地',
   description          text comment '用户个人描述',
   url                  varchar(128) comment '用户博客地址',
   profile_url          varchar(128) comment '用户微博统一URL地址',
   user_domain          varchar(32) comment '用户个性化域名',
   weihao               varchar(32) comment '用户微号',
   gender               char(1) not null comment 'm男，f女，n未知',
   followers_count      int not null,
   bi_followers_count   int not null comment '用户的互粉数',
   friends_count        int not null,
   statuses_count       int not null,
   favourites_count     int not null,
   ucreate_at           varchar(64) comment '用户注册时间',
   allow_all_act_msg    bool comment '是否允许所有人给我发私信',
   geo_enabled          bool comment '是否允许标识用户的地理位置',
   verified             bool not null comment '是否是微博认证用户',
   allow_all_comment    bool comment '是否允许所有人对我的微博进行评论',
   verified_reason      text comment '认证原因',
   primary key (userid)
);

alter table comments add constraint FK_commented_by foreign key (userid)
      references users (userid) on delete restrict on update restrict;

alter table comments add constraint FK_comments_for foreign key (sid)
      references status (sid) on delete restrict on update restrict;

alter table comments add constraint FK_reply2 foreign key (reply2Id)
      references comments (cid) on delete restrict on update restrict;

alter table status add constraint FK_locates foreign key (gid)
      references geo (gid) on delete restrict on update restrict;

alter table status add constraint FK_released_by foreign key (userid)
      references users (userid) on delete restrict on update restrict;

alter table status add constraint FK_retweet foreign key (retweetOfId)
      references status (sid) on delete restrict on update restrict;


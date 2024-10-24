import ConnectorSingleton from '../connection/connector_singleton';
import {
  Application,
  Context,
  Seed,
  SeedTypeEnum,
} from '@pieces.app/pieces-os-client';
import Notifications from '../connection/notification_handler';
import Constants from '../const';
import { SegmentAnalytics } from '../analytics/SegmentAnalytics';
import { AnalyticsEnum } from '../analytics/AnalyticsEnum';
import { launchRuntime } from './launch_runtime';
import { Annotation } from '@pieces.app/pieces-os-client';
import { PageConfig } from '@jupyterlab/coreutils';
import { AnchorTypeEnum } from '@pieces.app/pieces-os-client';

export default async function createAsset({
  selection,
  retry = false,
  name,
  annotations,
  lang,
  filePath,
  anchors,
}: {
  selection: string;
  retry?: boolean;
  name?: string;
  annotations?: Annotation[];
  lang?: string;
  filePath?: string;
  anchors?: string[];
}): Promise<void | string> {
  const root = PageConfig.getOption('serverRoot');

  SegmentAnalytics.track({
    event: AnalyticsEnum.JUPYTER_USER_SAVE,
  });

  const config: ConnectorSingleton = ConnectorSingleton.getInstance();
  const notifications: Notifications = Notifications.getInstance();
  let context: Context | undefined = config.context;
  try {
    config.context = await config.api.connect({
      seededConnectorConnection: config.seeded,
    });
    context = config.context;
  } catch (error) {
    notifications.error({ message: Constants.CONNECTION_FAIL });
    SegmentAnalytics.track({
      event: AnalyticsEnum.JUPYTER_SAVE_FAILURE,
    });
    return Promise.reject(new Error('Failed to Connect'));
  }

  const application: Application | undefined = context?.application;
  if (!application) return;

  const seededConnectorCreation: Seed = {
    type: SeedTypeEnum.Asset,
    asset: {
      application,
      format: {
        fragment: {
          string: {
            raw: selection,
          },
        },
      },
    },
  };

  // TODO REIMPLEMENT THIS SO WE CAN CHECK WHAT LANGUAGE
  //    -- it might always be python, need to double check.
  // if (lang && lang.length) {
  // 	//@ts-ignore we know that .asset.format exists here
  // 	seededConnectorCreation.asset.format.fragment.metadata = {
  // 		ext: invertedSearchLangSpecificEnum[
  // 			lang.toLowerCase()
  // 		] as ClassificationSpecificEnum,
  // 	};
  // }

  seededConnectorCreation.asset!.metadata = {};
  if (name && name.length) {
    seededConnectorCreation.asset!.metadata = {
      ...seededConnectorCreation.asset!.metadata,
      name: name,
    };
  }
  if (annotations && annotations.length) {
    seededConnectorCreation.asset!.metadata = {
      ...seededConnectorCreation.asset!.metadata,
      annotations: annotations.map((annotation) => {
        return {
          type: annotation.type,
          text: annotation.text,
          mechanism: annotation.mechanism,
          asset: annotation.asset?.id,
        };
      }),
    };
  }

  if (filePath && filePath !== 'unknown') {
    seededConnectorCreation.asset!.metadata!.anchors = [
      {
        type: AnchorTypeEnum.File,
        fullpath: root + '/' + filePath,
      },
    ];
  }

  if (anchors?.length) {
    if (!seededConnectorCreation.asset!.metadata.anchors)
      seededConnectorCreation.asset!.metadata.anchors = [];
    for (let anchor of anchors) {
      seededConnectorCreation.asset!.metadata!.anchors.push({
        fullpath: anchor,
        type: AnchorTypeEnum.File,
      });
    }
  }

  try {
    const asset = await config.assetsApi.assetsCreateNewAsset({
      seed: seededConnectorCreation,
    });
    notifications.information({ message: Constants.SAVE_SUCCESS });
    SegmentAnalytics.track({
      event: AnalyticsEnum.JUPYTER_SAVE_SUCCESS,
    });
    return asset.id;
  } catch (error: any) {
    if (retry) {
      notifications.error({ message: Constants.SAVE_FAIL });
      SegmentAnalytics.track({
        event: AnalyticsEnum.JUPYTER_SAVE_FAILURE,
      });
      return Promise.reject(new Error(`Error saving piece ${error.message}`));
    }
    if (error.status === 401 || error.status === 400) {
      SegmentAnalytics.track({
        event: AnalyticsEnum.JUPYTER_SAVE_FAILURE,
      });
      return Promise.reject(
        new Error(`User error reported from POS ${error.status}`)
      );
    }
    if (error.code === 'ECONNREFUSED') {
      if (retry) {
        SegmentAnalytics.track({
          event: AnalyticsEnum.JUPYTER_SAVE_FAILURE,
        });
        return Promise.reject(new Error(`Error saving piece ${error.message}`));
      }
      // attempt to launch runtime because we could talk to POS
      await launchRuntime(true);
      config.context = await config.api.connect({
        seededConnectorConnection: config.seeded,
      });
    }

    return await createAsset({ selection: selection, retry: true });
  }
}
